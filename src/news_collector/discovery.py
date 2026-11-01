import gzip
import io
from urllib.parse import urljoin

import feedparser
from bs4 import BeautifulSoup
from lxml import etree

from .fetching import Client, CrawlError
from .models import now
from .processing import article_url, normalize_url, same_site


def parse_xml(data: bytes, max_bytes: int = 10_000_000):
    if data.startswith(b"\x1f\x8b"):
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
            data = stream.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("XML exceeds size limit")
    root = etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True))
    if root.getroottree().docinfo.doctype:
        raise ValueError("XML DTD is not supported")
    return root, data


def parse_endpoint(data: bytes, method: str) -> tuple[list[dict], list[str]]:
    root, data = parse_xml(data)
    name = etree.QName(root).localname
    if method == "rss":
        if name not in {"rss", "feed", "RDF"}:
            raise ValueError("Not RSS/Atom XML")
        feed = feedparser.parse(data)
        return [{"url": e.link, "title": e.get("title"),
                 "published_at": e.get("published"), "description": e.get("summary")}
                for e in feed.entries if e.get("link")], []
    if name == "sitemapindex":
        return [], root.xpath("./*[local-name()='sitemap']/*[local-name()='loc']/text()")
    if name != "urlset":
        raise ValueError("Not a sitemap XML")
    entries = []
    for node in root:
        loc = node.xpath("./*[local-name()='loc']/text()")
        if loc:
            # lastmod is intentionally NOT a publication date.
            dates = node.xpath(".//*[local-name()='publication_date']/text()")
            entries.append({"url": loc[0], "published_at": dates[0] if dates else None})
    return entries, []

def relevant_endpoint(url: str) -> bool:
    lowered = url.lower()
    return not any(token in lowered for token in ("du-lich", "ban-doc", "video", "audio", "bat-dong-san", "real-estate"))


async def candidates(client: Client, source: dict) -> tuple[list[dict], list[dict]]:
    base = source["base_url"]
    errors, result = [], [e for e in source.get("endpoints", []) if relevant_endpoint(e["url"])]
    try:
        policy = await client.robots(base)
        result += [{"url": u, "method": "sitemap"} for u in policy.site_maps() or [] if same_site(u, base)]
    except CrawlError as exc:
        errors.append({"url": base + "/robots.txt", "status": exc.status, "error": str(exc)})
        return result, errors
    for page in source.get("rss_pages", []):
        try:
            r = await client.get(page, base)
            soup = BeautifulSoup(r.content, "html.parser")
            links = []
            for tag in soup.select("a[href], link[href]"):
                href = urljoin(str(r.url), tag["href"])
                if same_site(href, base) and ("rss" in tag.get("type", "") or "atom" in tag.get("type", "")
                                             or href.endswith(".rss") or href.rstrip("/").endswith("/feed")):
                    links.append(href)
            links.sort(key=lambda u: (not any(k in u for k in ["kinh-doanh", "kinh-te", "/feed/"]), u))
            result += [{"url": u, "method": "rss"} for u in links[:3]]
        except CrawlError as exc:
            errors.append({"url": page, "status": exc.status, "error": str(exc)})
    unique = {}
    for endpoint in result:
        unique[(endpoint["url"], endpoint["method"])] = endpoint
    feeds = [e for e in unique.values() if e["method"] == "rss"]
    maps = [e for e in unique.values() if e["method"] == "sitemap"]
    # News/latest maps are the most useful for a small feasibility sample.
    maps.sort(key=lambda e: (not any(k in e["url"] for k in ["news", "latest"]), e["url"]))
    return feeds[:3] + maps[:client.s.max_sitemap_roots], errors


async def inspect_endpoint(client: Client, source: dict, endpoint: dict) -> tuple[list[dict], list[dict]]:
    queue = [(endpoint["url"], 0)]
    visited, entries, evidence = set(), [], []
    while queue and len(visited) < client.s.max_sitemaps and len(entries) < client.s.max_urls_per_source:
        url, depth = queue.pop(0)
        if url in visited or depth > client.s.max_sitemap_depth:
            continue
        visited.add(url)
        item = {"url": url, "method": endpoint["method"], "checked_at": now()}
        try:
            r = await client.get(url, source["base_url"])
            item.update(http_status=r.status_code, content_type=r.headers.get("content-type", ""))
            found, children = parse_endpoint(r.content, endpoint["method"])
            valid = []
            for entry in found:
                if article_url(entry["url"], source):
                    valid.append(dict(entry, url=normalize_url(entry["url"]), endpoint=url, method=endpoint["method"]))
            entries.extend(valid[:client.s.max_urls_per_source - len(entries)])
            item.update(status="available" if valid else "unknown", article_urls=len(valid), child_sitemaps=len(children))
            queue += [(u, depth + 1) for u in children if same_site(u, source["base_url"])]
        except (CrawlError, ValueError, etree.XMLSyntaxError, OSError, EOFError) as exc:
            item.update(status=("restricted" if exc.status == "restricted" else "unavailable")
                        if isinstance(exc, CrawlError) else "unavailable", error=str(exc))
            if isinstance(exc, CrawlError):
                item["http_status"] = exc.http_status
        evidence.append(item)
    if entries and evidence:
        evidence[0]["status"] = "available"
    return entries, evidence
