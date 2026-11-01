import json
from datetime import timezone
from urllib.parse import urljoin

import trafilatura
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

from .fetching import CrawlError
from .models import Article
from .processing import clean_text, digest, normalize_url, relevance, same_site


def utc_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        date = parse_date(value)
        return date.astimezone(timezone.utc).isoformat() if date.tzinfo else None
    except (ValueError, TypeError, OverflowError):
        return None


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def extract(html: bytes, url: str, source_id: str, source: dict, discovery: dict,
            keywords: list[str], min_words: int) -> Article:
    soup = BeautifulSoup(html, "html.parser")

    def meta(key):
        tag = soup.find("meta", attrs={"property": key}) or soup.find("meta", attrs={"name": key})
        return tag.get("content") if tag else None

    ld = {}
    for script in soup.select('script[type="application/ld+json"]'):
        try:
            for obj in objects(json.loads(script.get_text())):
                kind = obj.get("@type", [])
                kind = [kind] if isinstance(kind, str) else kind
                if any(k in {"NewsArticle", "Article", "BlogPosting"} for k in kind):
                    ld = obj
                    break
        except (ValueError, TypeError):
            continue
    title = ld.get("headline") or meta("og:title") or (soup.h1.get_text(" ", strip=True) if soup.h1 else None)
    screen = (soup.title.get_text(" ", strip=True) if soup.title else "").lower()
    diagnostics = []
    restricted = ld.get("isAccessibleForFree") in (False, "false", "False")
    if restricted: diagnostics.append({"signal":"jsonld_accessible_for_free","value":False})
    def visible(tag):
        if tag.name in {"script", "style", "template", "noscript"}:
            return False
        classes = " ".join(tag.get("class", []))
        style = (tag.get("style") or "").replace(" ", "").lower()
        return "hidden" not in classes.lower() and "display:none" not in style and "visibility:hidden" not in style
    challenge = [tag for tag in soup.select('[id*="captcha"], .g-recaptcha, #challenge-running, [data-testid="paywall"], [class*="paywall"]') if visible(tag)]
    # Login/comment CAPTCHA widgets are commonly present on otherwise public articles.
    # They are evidence of a challenge only when no substantial article body exists.
    article_text = " ".join(x.get_text(" ", strip=True) for x in soup.select("article, .detail-content, .fck_detail, .entry-content"))
    if len(article_text.split()) >= 80:
        challenge = [tag for tag in challenge if not ("captcha" in str(tag.get("id", "")).lower() or "captcha" in " ".join(tag.get("class", [])).lower() or tag.get("class") == ["resetcaptcha"])]
    if challenge: diagnostics.append({"signal":"challenge_or_paywall_selector","count":len(challenge)})
    if any(x in screen for x in ["just a moment", "access denied", "are you a robot", "verify you are human"]):
        diagnostics.append({"signal":"challenge_title","title":screen[:200]})
    restricted |= bool(diagnostics)
    if restricted:
        error = CrawlError("restricted", "Paywall/login/bot challenge detected")
        error.diagnostics = diagnostics
        raise error
    text = trafilatura.extract(html, url=url, include_comments=False, include_tables=False) or ""
    method = "trafilatura"
    if len(text.split()) < min_words:
        selectors = {"vnexpress": ".fck_detail", "tuoitre": ".detail-content", "techcrunch": ".entry-content"}
        node = soup.select_one(selectors.get(source_id, "article"))
        if node:
            text = "\n".join(p.get_text(" ", strip=True) for p in node.select("p"))
            method = "site_rule"
    if not title or len(text.split()) < min_words:
        raise CrawlError("extraction_failed", f"Missing title or content below {min_words} words")
    canonical_tag = soup.find("link", rel="canonical")
    canonical = urljoin(url, canonical_tag.get("href", "")) if canonical_tag else url
    canonical = normalize_url(canonical if same_site(canonical, source["base_url"]) else url)
    published = utc_date(ld.get("datePublished") or meta("article:published_time") or meta("pubdate") or discovery.get("published_at"))
    authors = ld.get("author") or meta("author") or []
    if not isinstance(authors, list):
        authors = [authors]
    authors = [a.get("name") if isinstance(a, dict) else a for a in authors]
    description = ld.get("description") or meta("description") or meta("og:description")
    tags = ld.get("keywords") or meta("keywords") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    return Article(article_id=digest(canonical), source=source_id, url=url, canonical_url=canonical,
                   title=clean_text(str(title)), description=description,
                   authors=[a for a in authors if isinstance(a, str) and a], published_at=published,
                   updated_at=utc_date(ld.get("dateModified") or meta("article:modified_time")),
                   language=source["language"], category=meta("article:section"), tags=tags,
                   content=text.strip(), word_count=len(text.split()), content_hash=digest(clean_text(text)),
                   discovery_method=discovery["method"], discovery_endpoint=discovery["endpoint"],
                   extraction_method=method, quality_flags=[] if published else ["missing_published_at"],
                   **relevance(str(title), description or "", text, keywords))
