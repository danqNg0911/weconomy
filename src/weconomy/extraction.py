"""Extract the visible article body, retain evidence, and quarantine uncertain content."""
import copy
import json
import re
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin, urlsplit

import trafilatura
from lxml import etree, html

from .access import canonical_url
from .nlp import normalize

EXTRACTOR_VERSION = "body-v2.1"
BLOCKS = {"article", "section", "div", "p", "li", "blockquote", "h1", "h2", "h3", "h4", "pre"}
NOISE_LABELS = {
    "related", "related-news", "related-articles", "recommended-posts", "recommendations",
    "comment", "comments", "comment-list", "comment-section", "advertisement", "advertisements",
    "advertising", "ad", "ads", "ad-container", "newsletter", "social-share", "social-sharing",
    "share-tools", "share-buttons", "caption", "photo-caption", "sharedaddy", "jp-relatedposts",
    "box-tin-lien-quan", "box-tin-tai-tro", "vcobjectboxrelatednewsitemsapo",
    "vcobjectboxrelatednewsitemtitle", "photocms_caption", "kbwscwl-relatedbox", "detail__related",
    "detail-comment", "detail_comment", "comment-wrapper", "detail-social",
}
GATE = re.compile(r"paywall|subscription-gate|content-gate|locked-content|premium-overlay|captcha|challenge-running", re.I)
TRUNCATION = re.compile(
    r"subscribe to (?:continue reading|read (?:the )?(?:full|rest))|"
    r"sign in to (?:continue reading|read (?:the )?full)|"
    r"đăng (?:ký|nhập) để (?:đọc tiếp|đọc toàn bộ)|mua gói để đọc tiếp", re.I)


def visible(node):
    for parent in [node, *node.iterancestors()]:
        if not isinstance(parent.tag, str):
            continue
        if parent.tag.lower() in {"script", "style", "template", "noscript"}:
            return False
        classes = set((parent.get("class") or "").lower().split())
        style = re.sub(r"\s+", "", parent.get("style", "")).lower()
        if ("hidden" in parent.attrib or parent.get("aria-hidden") == "true"
                or classes & {"hidden", "is-hidden", "d-none", "hide"}
                or "display:none" in style or "visibility:hidden" in style):
            return False
    return True


def auxiliary(node):
    labels = set(node.get("class", "").lower().split()) | {node.get("id", "").lower()}
    return bool(labels & NOISE_LABELS)


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def tokens(text):
    return " ".join(re.findall(r"\w+", text.casefold()))


def utc_date(value):
    try:
        try:
            date = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            date = parsedate_to_datetime(str(value))
        return date.astimezone(UTC).isoformat() if date.tzinfo else ""
    except (ValueError, TypeError, OverflowError):
        return ""


def metadata(tree, url, source):
    def meta(name):
        return next(iter(tree.xpath("//meta[@name=$n or @property=$n]/@content", n=name)), "")

    canonical = url
    for href in tree.xpath("//link[@rel='canonical']/@href"):
        candidate = urljoin(url, href)
        if urlsplit(candidate).hostname in source.get("hosts", [urlsplit(url).hostname]):
            try:
                canonical = canonical_url(candidate)
            except ValueError:
                pass
            break
    h1 = next(iter(tree.xpath("//h1")), None)
    heading = normalize(h1.text_content()) if h1 is not None else ""
    candidates = []
    for script in tree.xpath("//script[@type='application/ld+json']"):
        try:
            for obj in objects(json.loads(script.text or "")):
                kinds = obj.get("@type") or []
                kinds = [kinds] if isinstance(kinds, str) else kinds
                if not set(kinds) & {"NewsArticle", "Article", "BlogPosting"}:
                    continue
                links = [obj.get("url"), obj.get("@id"), obj.get("mainEntityOfPage")]
                targets = []
                for link in links:
                    if isinstance(link, dict):
                        link = link.get("@id") or link.get("url")
                    if isinstance(link, str):
                        try:
                            targets.append(canonical_url(urljoin(url, link)))
                        except ValueError:
                            continue
                matched = bool({canonical, canonical_url(url)} & set(targets))
                if targets and not matched:
                    continue
                headline_match = bool(heading and tokens(str(obj.get("headline", ""))) == tokens(heading))
                candidates.append((100 * matched + 10 * headline_match, obj))
        except (ValueError, TypeError):
            continue
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    # Preserve consensus metadata across duplicates, and restriction even when other fields conflict.
    top = [obj for score, obj in candidates if score == candidates[0][0]] if candidates else []
    identified = [obj for score, obj in candidates if score >= 100] or top
    restricted = any(obj.get("isAccessibleForFree") in (False, "false", "False") for obj in identified)
    ld = {}
    for key in {key for obj in top for key in obj}:
        values = [obj.get(key) for obj in top]
        if all(value == values[0] for value in values):
            ld[key] = values[0]
    authors = ld.get("author") or meta("author") or []
    authors = authors if isinstance(authors, list) else [authors]
    authors = [a.get("name", "") if isinstance(a, dict) else a for a in authors]
    title = ld.get("headline") or meta("og:title") or heading or tree.findtext(".//title") or ""
    return {"title": normalize(str(title)), "canonical_url": canonical,
            "published_at": utc_date(ld.get("datePublished") or meta("article:published_time")),
            "authors": [a for a in authors if isinstance(a, str) and a],
            "restricted_metadata": restricted}


def clean_body(node):
    node = copy.deepcopy(node)
    # Inspect visibility before removing ancestors; an ordinary descendant of a hidden div is hidden too.
    remove = [child for child in node.iterdescendants() if isinstance(child.tag, str) and
              (not visible(child) or child.tag.lower() in
               {"script", "style", "template", "noscript", "nav", "aside", "footer", "form", "button",
                "figure", "figcaption", "table", "iframe"}
               or auxiliary(child))]
    for child in remove:
        if child.getparent() is not None:
            child.drop_tree()
    return node


def body_paragraphs(node):
    parts = []

    def walk(element):
        if not isinstance(element.tag, str):
            return
        block = element.tag.lower() in BLOCKS
        if block:
            parts.append("\n")
        if element.text:
            parts.append(re.sub(r"\s+", " ", element.text))
        for child in element:
            walk(child)
            if child.tail:
                parts.append(re.sub(r"\s+", " ", child.tail))
        if block or element.tag.lower() == "br":
            parts.append("\n")

    walk(node)
    return [line for line in normalize("".join(parts)).splitlines() if line]


def extract_article(raw, url, source, config, *, capture_scope="full_page"):
    parser_options = {"remove_comments": True, "no_network": True}
    if isinstance(raw, bytes):
        try:
            raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            pass  # Non-UTF-8 archives still use their own declared charset.
        else:
            parser_options["encoding"] = "utf-8"
    tree = html.document_fromstring(raw, parser=html.HTMLParser(**parser_options))
    info = metadata(tree, url, source)
    body_xpath = source.get("body_xpath", "")
    bodies = tree.xpath(body_xpath) if body_xpath else []
    bodies = [body for body in bodies if visible(body)]
    known_body = bool(bodies)
    if not bodies:
        bodies = [body for body in tree.xpath("//article") if visible(body)]
    body = max(bodies, key=lambda n: len(n.text_content())) if bodies else tree
    flags = []
    screen = (tree.findtext(".//title") or "").casefold()
    if any(word in screen for word in ("just a moment", "access denied", "verify you are human")):
        flags.append("challenge_page")
    if info.pop("restricted_metadata"):
        flags.append("restricted_article_metadata")
    for node in tree.iter():
        if not isinstance(node.tag, str) or not visible(node):
            continue
        if any(auxiliary(parent) for parent in [node, *node.iterancestors()]):
            continue
        label = " ".join([node.get("class", ""), node.get("id", ""), node.get("data-testid", "")])
        in_body = node is body or any(parent is body for parent in node.iterancestors())
        # Comment/login CAPTCHA outside the article is not evidence that the article itself is gated.
        if GATE.search(label) and ("captcha" not in label.lower() or in_body):
            flags.append("visible_access_gate")
            break
    cleaned = clean_body(body)
    paragraphs = body_paragraphs(cleaned)
    dom_text = "\n".join(paragraphs)
    if TRUNCATION.search(dom_text):
        flags.append("explicit_truncation_notice")
    candidate = trafilatura.extract(etree.tostring(cleaned, encoding="unicode"), url=url,
                                     include_comments=False, include_tables=False, favor_precision=True) or ""
    candidate = normalize(candidate)
    sequence = tokens(candidate)
    matches = sum(tokens(p) in sequence for p in paragraphs)
    coverage = matches / len(paragraphs) if paragraphs else 0.0
    if known_body and coverage < 1:
        text, method = dom_text, "source_dom_recovery"
    elif known_body:
        text, method = candidate, "trafilatura_body_checked"
    else:
        text, method = candidate, "trafilatura_unverified_body"
    if capture_scope == "excerpt":
        # Diagnostic sample runs remain possible, but cannot count as collected full articles.
        text = text or dom_text
        status = "excerpt"
    elif flags:
        status = "restricted" if any(f in flags for f in
                                     ("visible_access_gate", "restricted_article_metadata", "challenge_page")) else "partial"
    elif not info["title"] or len(text.split()) < config.get("min_article_words", 100):
        status = "partial"
        flags.append("insufficient_article_body")
    elif not known_body:
        status = "unknown"
        flags.append("unverified_body_selector")
    else:
        status = "body_checked"
    eligible = status == "body_checked" or (status == "excerpt" and config.get("allow_excerpts", False) and not flags)
    return {**info, "text": text, "content_status": status, "extraction_method": method,
            "extractor_version": EXTRACTOR_VERSION, "word_count": len(text.split()),
            "body_paragraphs": len(paragraphs), "trafilatura_coverage": coverage,
            "paragraph_coverage": 1.0 if known_body and paragraphs else None,
            "quality_flags": flags, "nlp_eligible": eligible}
