import hashlib
import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    p = urlsplit(url.strip())
    if p.scheme.lower() not in {"http", "https"} or not p.hostname or p.username or p.password:
        raise ValueError("Invalid HTTP URL")
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid"}]
    host = p.hostname.lower()
    if p.port and not (p.scheme == "https" and p.port == 443 or p.scheme == "http" and p.port == 80):
        host += f":{p.port}"
    return urlunsplit((p.scheme.lower(), host, p.path or "/", urlencode(query), ""))


def same_site(url: str, base: str) -> bool:
    try:
        p, b = urlsplit(normalize_url(url)), urlsplit(base)
        return p.hostname.removeprefix("www.") == b.hostname.removeprefix("www.") and p.port in {None, 80, 443}
    except (ValueError, AttributeError):
        return False


def article_url(url: str, source: dict) -> bool:
    return same_site(url, source["base_url"]) and bool(re.search(source["article_pattern"], urlsplit(url).path))


def clean_text(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


INTERNATIONAL = ["international", "global", "cross-border", "cross border", "overseas", "worldwide", "quốc tế", "xuyên biên giới"]
DOMESTIC = ["trong nước", "nội địa", "domestic", "local market", "tỉnh", "huyện"]

def relevance(title: str, description: str, content: str, keywords: list[str]) -> dict:
    score, matched = 0, []
    for keyword in keywords:
        pattern = r"(?<!\w)" + re.escape(keyword.casefold()) + r"(?!\w)"
        points = sum(weight for text, weight in [(title, 3), (description, 2), (content, 1)]
                     if re.search(pattern, text.casefold()))
        if points:
            score += points
            matched.append(keyword)
    text = f"{title} {description} {content}".casefold()
    intl = any(k.casefold() in text for k in INTERNATIONAL)
    domestic = any(k.casefold() in text for k in DOMESTIC)
    scope = "international" if intl and score >= 3 else "domestic_only" if domestic and not intl and score < 3 else "cross_border" if intl and score else "uncertain"
    return {"relevance_score": score, "matched_keywords": matched,
            "relevance_status": "relevant" if score >= 3 else "review" if score else "irrelevant",
            "topic_scope": scope, "geographic_scope": "international" if intl else "domestic" if domestic else "uncertain"}
