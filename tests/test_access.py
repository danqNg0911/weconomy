from pathlib import Path

import httpx
import pytest

from weconomy.access import Access, canonical_url, katana_urls
from weconomy.pipeline import load_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("url", ["http://example.org", "file:///etc/passwd", "https://user:pass@x.org/",
                                 "https://x.org:8080/"])
def test_rejects_unsafe_urls(url):
    with pytest.raises(ValueError):
        canonical_url(url)


def test_normalizes_only_tracking():
    assert canonical_url("https://EN.wikinews.org/wiki/X?oldid=123&utm_source=y#x") == (
        "https://en.wikinews.org/wiki/X?oldid=123")


def test_disabled_source_no_request():
    access = Access(load_config(ROOT / "config/pipeline.yaml"))
    try:
        with pytest.raises(PermissionError, match="Source disabled"):
            access.fetch("https://www.reuters.com/world/")
        with pytest.raises(PermissionError, match="Unknown"):
            access.fetch("https://localhost/")
    finally:
        access.close()


@pytest.mark.parametrize("source, url", [
    ("wikinews_en", "https://en.wikinews.org/wiki/X"),
    ("techcrunch", "https://techcrunch.com/2026/01/01/example/"),
])
def test_disabled_source_policy_rejects_before_request(source, url):
    access = Access(load_config(ROOT / "config/pipeline.yaml"))

    def fail_if_requested(request):
        raise AssertionError(f"Unexpected request: {request.url}")

    access.client.close()
    access.client = httpx.Client(transport=httpx.MockTransport(fail_if_requested))
    try:
        with pytest.raises(PermissionError, match="Source disabled"):
            access.fetch(url)
        with pytest.raises(PermissionError, match="Source disabled"):
            access.discover(source, 1)
    finally:
        access.close()


def mock_access(monkeypatch, handler):
    access = Access(load_config(ROOT / "config/pipeline.yaml"))
    monkeypatch.setattr("weconomy.access.socket.getaddrinfo", lambda *a, **k: [(2, 1, 6, "", ("8.8.8.8", 443))])
    # Synthetic Wikinews fixture access is enabled here only; production policy stays disabled.
    access.sources["wikinews_en"]["allowed"] = True
    access.sources["wikinews_en"]["feeds"] = ["https://en.wikinews.org/fixture.rss"]
    access.sources["wikinews_en"]["min_interval_seconds"] = 0
    access.client.close()
    access.client = httpx.Client(transport=httpx.MockTransport(handler))
    return access


def test_robots_denies_before_page_download(monkeypatch):
    seen = []

    def handler(request):
        seen.append(str(request.url))
        return httpx.Response(200, text="User-agent: *\nDisallow: /wiki/")

    access = mock_access(monkeypatch, handler)
    try:
        with pytest.raises(PermissionError, match="robots"):
            access.fetch("https://en.wikinews.org/wiki/X")
        assert len(seen) == 1
    finally:
        access.close()


def test_redirect_cannot_escape_policy(monkeypatch):
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        return httpx.Response(302, headers={"location": "https://evil.example/secret"})

    access = mock_access(monkeypatch, handler)
    try:
        with pytest.raises(PermissionError, match="Unknown"):
            access.fetch("https://en.wikinews.org/wiki/X")
    finally:
        access.close()


@pytest.mark.parametrize("status", [403, 429])
def test_access_denial_or_rate_limit_pauses_only_that_host(monkeypatch, status):
    seen = []

    def handler(request):
        seen.append(request.url.host)
        return httpx.Response(status if request.url.host == "en.wikinews.org" else 200)

    access = mock_access(monkeypatch, handler)
    try:
        with pytest.raises(httpx.HTTPStatusError):
            access._request("https://en.wikinews.org/first", 0)
        with pytest.raises(PermissionError, match=f"HTTP {status}"):
            access._request("https://en.wikinews.org/second", 0)
        assert access._request("https://other.example/ok", 0)[0] == 200
        assert seen == ["en.wikinews.org", "other.example"]
    finally:
        access.close()


def test_rss_discovery(monkeypatch):
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        return httpx.Response(200, text='''<rss version="2.0"><channel><title>Fixture</title>
            <item><link>https://en.wikinews.org/wiki/One</link></item>
            <item><link>https://en.wikinews.org/wiki/One?utm_source=x</link></item>
            </channel></rss>''')

    access = mock_access(monkeypatch, handler)
    try:
        assert access.discover("wikinews_en", 2) == ["https://en.wikinews.org/wiki/One"]
        assert access.discover_records("wikinews_en", 2, exclude_urls={
            "https://en.wikinews.org/wiki/One"}) == []
    finally:
        access.close()


def test_katana_import(tmp_path):
    path = tmp_path / "katana.jsonl"
    path.write_text('{"request":{"endpoint":"https://en.wikinews.org/wiki/X"}}\n', encoding="utf-8")
    assert katana_urls(path) == ["https://en.wikinews.org/wiki/X"]
