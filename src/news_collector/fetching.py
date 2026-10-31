"""Sequential, bounded HTTP with robots checks on every redirect destination."""
import asyncio
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

import httpx

from .config import Settings
from .processing import same_site


class CrawlError(Exception):
    def __init__(self, status: str, message: str, http_status: int | None = None,
                 retry_at: str | None = None):
        super().__init__(message)
        self.status, self.http_status, self.retry_at = status, http_status, retry_at
        self.diagnostics = []


class Client:
    def __init__(self, settings: Settings, transport=None):
        self.s = settings
        self.http = httpx.AsyncClient(timeout=settings.timeout_seconds,
                                     headers={"User-Agent": settings.user_agent}, transport=transport)
        self.policies: dict[str, RobotFileParser] = {}
        self.last: dict[str, float] = {}
        self.paused: dict[str, CrawlError] = {}
        self.robots_evidence: dict[str, dict] = {}

    async def close(self):
        await self.http.aclose()

    async def _request(self, url: str, delay: float) -> httpx.Response:
        host = urlsplit(url).netloc
        if host in self.paused:
            raise self.paused[host]
        for attempt in range(self.s.max_retries + 1):
            await asyncio.sleep(max(0, self.last.get(host, 0) + delay - time.monotonic()))
            self.last[host] = time.monotonic()
            try:
                async with self.http.stream("GET", url) as response:
                    parts, size = [], 0
                    async for chunk in response.aiter_bytes():
                        size += len(chunk)
                        if size > self.s.max_response_bytes:
                            raise CrawlError("fetch_failed", "Response exceeds byte limit")
                        parts.append(chunk)
                    # aiter_bytes() already decoded compression; avoid decoding twice.
                    headers = {k: v for k, v in response.headers.items()
                               if k.lower() not in {"content-encoding", "content-length"}}
                    r = httpx.Response(response.status_code, headers=headers,
                                       content=b"".join(parts), request=response.request)
            except httpx.RequestError as exc:
                if attempt == self.s.max_retries:
                    raise CrawlError("fetch_failed", str(exc)) from exc
                await asyncio.sleep(2 ** attempt)
                continue
            if r.status_code == 429:
                value = r.headers.get("retry-after", "60")
                try:
                    retry = datetime.fromtimestamp(time.time() + max(0, int(value)), timezone.utc)
                except ValueError:
                    try:
                        retry = parsedate_to_datetime(value)
                    except (ValueError, TypeError):
                        retry = datetime.fromtimestamp(time.time() + 60, timezone.utc)
                error = CrawlError("fetch_failed", "Rate limited; source paused for this run", 429, retry.isoformat())
                self.paused[host] = error
                raise error
            if r.status_code >= 500 and attempt < self.s.max_retries:
                await asyncio.sleep(2 ** attempt)
                continue
            return r
        raise AssertionError("unreachable")

    async def robots(self, base: str) -> RobotFileParser:
        p = urlsplit(base)
        origin = f"{p.scheme}://{p.netloc}"
        if origin in self.policies:
            return self.policies[origin]
        url = origin + "/robots.txt"
        r = await self._request(url, self.s.delay_seconds)
        for _ in range(4):
            if not r.is_redirect:
                break
            target = urljoin(str(r.url), r.headers.get("location", ""))
            if not same_site(target, base) or urlsplit(target).path != "/robots.txt":
                raise CrawlError("restricted", "Unsafe robots redirect", r.status_code)
            r = await self._request(target, self.s.delay_seconds)
        parser = RobotFileParser(url)
        if r.status_code in {404, 410}:
            parser.parse([])
        elif r.status_code == 200 and "<html" not in r.text[:1000].lower():
            parser.parse(r.text.splitlines())
        else:
            raise CrawlError("restricted" if r.status_code in {401, 403} else "fetch_failed",
                             "robots.txt unavailable; permission unknown", r.status_code)
        self.robots_evidence[origin] = {"url": str(r.url), "http_status": r.status_code,
                                        "text": r.text[:100000]}
        self.policies[origin] = parser
        return parser

    async def get(self, url: str, base: str) -> httpx.Response:
        for _ in range(6):
            if not same_site(url, base):
                raise CrawlError("restricted", "Off-domain URL/redirect refused")
            policy = await self.robots(url)
            if not policy.can_fetch(self.s.user_agent, url):
                raise CrawlError("restricted", "Disallowed by robots.txt")
            delay = max(self.s.delay_seconds, policy.crawl_delay(self.s.user_agent) or 0)
            rate = policy.request_rate(self.s.user_agent)
            if rate and rate.requests:
                delay = max(delay, rate.seconds / rate.requests)
            r = await self._request(url, delay)
            if r.is_redirect:
                url = urljoin(url, r.headers.get("location", ""))
                continue
            if r.status_code in {401, 403, 451}:
                raise CrawlError("restricted", f"HTTP {r.status_code}", r.status_code)
            if r.status_code != 200:
                raise CrawlError("fetch_failed", f"HTTP {r.status_code}", r.status_code)
            return r
        raise CrawlError("fetch_failed", "Too many redirects")
