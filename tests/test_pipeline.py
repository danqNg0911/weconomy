import asyncio
import json

import httpx
import yaml

from news_collector import pipeline
from news_collector.config import Settings
from news_collector.discovery import inspect_endpoint
from news_collector.fetching import Client
from news_collector.storage import Store


def test_pilot_cap_resume_and_export(tmp_path, monkeypatch):
    calls = []
    def handler(request):
        path = request.url.path
        calls.append(path)
        if path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        if path == "/feed":
            items = "".join(f"<item><title>Story {i}</title><link>https://example.com/story/{i}</link></item>" for i in range(15))
            return httpx.Response(200, text=f"<rss version='2.0'><channel>{items}</channel></rss>", headers={"Content-Type": "application/rss+xml"})
        words = " ".join(f"unique{path[-2:]}word{i}" for i in range(120))
        return httpx.Response(200, text=f"<html><head><title>Story {path}</title></head><body><article><h1>Story {path}</h1><p>{words}</p></article></body></html>")
    settings = Settings(data_dir=tmp_path / "data", delay_seconds=0)
    sources = {"sample": {"base_url": "https://example.com", "language": "en", "article_pattern": "/story/",
                          "rss_pages": [], "endpoints": [{"url": "https://example.com/feed", "method": "rss"}]}}
    config = tmp_path / "configs"
    config.mkdir()
    monkeypatch.setattr(pipeline, "Client", lambda s: Client(s, httpx.MockTransport(handler)))
    first = asyncio.run(pipeline.execute(settings, sources, [], config, ["sample"], "run"))
    assert first["sources"]["sample"]["saved_total"] == 10
    assert first["sources"]["sample"]["attempted"] == 10
    count = len(calls)
    second = asyncio.run(pipeline.execute(settings, sources, [], config, ["sample"], "run"))
    assert second["sources"]["sample"]["saved_this_run"] == 0
    assert len(calls) == count
    values = [json.loads(line) for line in (settings.data_dir / "exports/articles.jsonl").read_text("utf-8").splitlines()]
    assert len(values) == len({v["article_id"] for v in values}) == 10
    assert yaml.safe_load((config / "sources.yaml").read_text("utf-8"))["sources"]["sample"]["status"] == "available"


def test_sitemap_cycles_depth_and_off_domain():
    calls = []
    def handler(request):
        calls.append(str(request.url))
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        if request.url.path == "/index.xml":
            return httpx.Response(200, text='<sitemapindex><sitemap><loc>https://example.com/index.xml</loc></sitemap><sitemap><loc>https://example.com/child.xml</loc></sitemap><sitemap><loc>https://evil.com/file.xml</loc></sitemap></sitemapindex>')
        return httpx.Response(200, text='<urlset><url><loc>https://example.com/story/1</loc></url></urlset>')
    async def check():
        client = Client(Settings(delay_seconds=0), httpx.MockTransport(handler))
        entries, evidence = await inspect_endpoint(client, {"base_url": "https://example.com", "article_pattern": "/story/"},
                                                  {"url": "https://example.com/index.xml", "method": "sitemap"})
        assert len(entries) == 1
        assert len(evidence) == 2
        assert not any("evil.com" in c for c in calls)
        assert calls.count("https://example.com/index.xml") == 1
        await client.close()
    asyncio.run(check())


def test_retry_server_error(monkeypatch):
    attempts = []
    sleeps = []
    async def sleep(delay):
        sleeps.append(delay)
    monkeypatch.setattr("news_collector.fetching.asyncio.sleep", sleep)
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        attempts.append(1)
        return httpx.Response(503 if len(attempts) < 3 else 200, text="ok")
    async def check():
        client = Client(Settings(delay_seconds=0, max_retries=2), httpx.MockTransport(handler))
        assert (await client.get("https://example.com/story", "https://example.com")).status_code == 200
        assert len(attempts) == 3
        assert 1 in sleeps and 2 in sleeps
        await client.close()
    asyncio.run(check())
