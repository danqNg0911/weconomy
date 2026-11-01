import asyncio
import gzip
import json

import httpx
import pytest
from typer.testing import CliRunner

from news_collector.cli import app
from news_collector.config import Settings
from news_collector.discovery import parse_endpoint
from news_collector.extraction import extract, utc_date
from news_collector.fetching import Client, CrawlError
from news_collector.processing import normalize_url, same_site
from news_collector.storage import Store

SOURCE = {"base_url": "https://example.com", "language": "en", "article_pattern": "/story"}
WORDS = " ".join(f"word{i}" for i in range(150))
HTML = ('<html><head><title>Investment update</title><link rel="canonical" href="/story"/>'
        '<script type="application/ld+json">{"@type":"NewsArticle","headline":"Investment update",'
        '"datePublished":"2026-01-01T12:00:00+07:00","author":{"name":"Reporter"}}</script>'
        '</head><body><article><h1>Investment update</h1><p>' + WORDS + '</p></article></body></html>').encode()


def article(url="https://example.com/story"):
    return extract(HTML, url, "test", SOURCE, {"method": "rss", "endpoint": "https://example.com/feed"}, ["investment"], 100)


def test_settings_and_url():
    with pytest.raises(ValueError):
        Settings(target_per_source=11)
    assert normalize_url("https://EXAMPLE.com/a?id=2&utm_source=x#frag") == "https://example.com/a?id=2"
    assert not same_site("https://example.com.evil.com/a", SOURCE["base_url"])
    assert not same_site("https://user:pw@example.com/a", SOURCE["base_url"])


@pytest.mark.parametrize("data", [
    b'<rss version="2.0"><channel><item><title>X</title><link>https://example.com/story</link></item></channel></rss>',
    b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>X</title><link href="https://example.com/story"/></entry></feed>',
])
def test_rss_atom(data):
    entries, children = parse_endpoint(data, "rss")
    assert entries[0]["url"] == "https://example.com/story"
    assert entries[0]["published_at"] is None
    assert not children


def test_sitemap_gzip_and_lastmod():
    xml = b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.com/story</loc><lastmod>2026-01-01</lastmod></url></urlset>'
    entries, _ = parse_endpoint(gzip.compress(xml), "sitemap")
    assert entries[0]["published_at"] is None
    _, children = parse_endpoint(b'<sitemapindex><sitemap><loc>https://example.com/child.xml</loc></sitemap></sitemapindex>', "sitemap")
    assert children == ["https://example.com/child.xml"]
    with pytest.raises(ValueError):
        parse_endpoint(b"<html/>", "rss")
    with pytest.raises(ValueError):
        parse_endpoint(b'<!DOCTYPE rss [<!ENTITY a "text">]><rss/>', "rss")


def test_extraction_metadata():
    a = article()
    assert a.published_at == "2026-01-01T05:00:00+00:00"
    assert a.authors == ["Reporter"]
    assert a.word_count >= 150
    assert a.relevance_status == "relevant"
    assert utc_date("2026-01-01") is None
    with pytest.raises(CrawlError, match="Paywall"):
        extract(HTML.replace(b'"@type":"NewsArticle"', b'"@type":"NewsArticle","isAccessibleForFree":false'),
                "https://example.com/story", "test", SOURCE, {}, [], 100)

def test_login_button_is_not_restriction_and_diagnostics_are_structured():
    html = HTML.replace(b"</body>", b'<button>Login</button><button>Subscribe</button></body>')
    discovery = {"method":"rss", "endpoint":"https://example.com/feed"}
    assert extract(html, "https://example.com/story", "test", SOURCE, discovery, [], 100).crawl_status == "success"
    paywall = HTML.replace(b"</body>", b'<div class="paywall">Subscribe to read</div></body>')
    with pytest.raises(CrawlError) as caught:
        extract(paywall, "https://example.com/story", "test", SOURCE, discovery, [], 100)
    assert caught.value.diagnostics[0]["signal"] == "challenge_or_paywall_selector"


def test_storage_dedup_and_recovery(tmp_path):
    store = Store(tmp_path)
    entries = [{"url": "https://example.com/story", "endpoint": "feed", "method": "rss"}]
    assert store.enqueue("test", entries) == 1
    assert store.enqueue("test", entries) == 0
    store.enqueue("test", [dict(entries[0], endpoint="sitemap", method="sitemap")])
    assert store.db.execute("SELECT count(*) FROM url_discoveries").fetchone()[0] == 2
    assert store.save(article(), entries[0]["url"])
    second = "https://example.com/story2"
    store.enqueue("test", [dict(entries[0], url=second)])
    assert not store.save(article(second), second)
    store.export().write_text("broken partial data", "utf-8")
    store.state("https://example.com/story2", "fetching")
    store.db.close()
    recovered = Store(tmp_path)
    assert len(recovered.export().read_text("utf-8").splitlines()) == 1
    assert recovered.count("test") == 1
    assert recovered.db.execute("SELECT status FROM url_queue WHERE url=?", (second,)).fetchone()[0] == "pending"
    recovered.db.close()


@pytest.mark.parametrize("code,status", [(403, "restricted"), (404, "fetch_failed"), (429, "fetch_failed"), (500, "fetch_failed")])
def test_http_errors(code, status):
    calls = []
    def handler(request):
        calls.append(str(request.url))
        return httpx.Response(200, text="User-agent: *\nAllow: /") if request.url.path == "/robots.txt" else httpx.Response(code, headers={"Retry-After": "120"})
    async def check():
        client = Client(Settings(delay_seconds=0, max_retries=0), httpx.MockTransport(handler))
        with pytest.raises(CrawlError) as err:
            await client.get("https://example.com/story", SOURCE["base_url"])
        assert err.value.status == status
        assert err.value.http_status == code
        if code == 429:
            assert err.value.retry_at
            with pytest.raises(CrawlError):
                await client.get("https://example.com/story2", SOURCE["base_url"])
            assert len(calls) == 2
        await client.close()
    asyncio.run(check())


def test_redirect_robots_and_timeout():
    calls = []
    def handler(request):
        calls.append(request.url.path)
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nDisallow: /private")
        if request.url.path == "/story":
            return httpx.Response(302, headers={"Location": "/private"})
        raise httpx.ReadTimeout("timeout", request=request)
    async def check():
        client = Client(Settings(delay_seconds=0, max_retries=0), httpx.MockTransport(handler))
        with pytest.raises(CrawlError, match="Disallowed"):
            await client.get("https://example.com/story", SOURCE["base_url"])
        assert "/private" not in calls
        with pytest.raises(CrawlError, match="timeout"):
            await client.get("https://example.com/timeout", SOURCE["base_url"])
        await client.close()
    asyncio.run(check())


def test_cli_rejects_large_pilot():
    result = CliRunner().invoke(app, ["run", "--all", "--limit", "11"])
    assert result.exit_code == 2
    assert "1..10" in result.output


def test_http_gzip_is_decoded_once():
    def handler(request):
        text = b"User-agent: *\nAllow: /" if request.url.path == "/robots.txt" else b"article payload"
        return httpx.Response(200, content=gzip.compress(text), headers={"Content-Encoding": "gzip"})
    async def check():
        client = Client(Settings(delay_seconds=0), httpx.MockTransport(handler))
        response = await client.get("https://example.com/story", SOURCE["base_url"])
        assert response.content == b"article payload"
        await client.close()
    asyncio.run(check())
