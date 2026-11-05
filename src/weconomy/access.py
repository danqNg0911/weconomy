"""One policy gate for feeds, pages and externally discovered URLs."""
import ipaddress
import json
import re
import socket
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import feedparser
import httpx
import yaml


def canonical_url(url: str) -> str:
    p = urlsplit(url)
    if p.scheme != "https" or not p.hostname or p.username or p.password or p.port not in (None, 443):
        raise ValueError("Only public HTTPS URLs on port 443 are allowed")
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid"}]
    return urlunsplit(("https", p.hostname.lower(), p.path or "/", urlencode(query), ""))


class Access:
    def __init__(self, config: dict):
        self.config = config
        self.sources = yaml.safe_load(Path(config["sources"]).read_text(encoding="utf-8"))["sources"]
        self.client = httpx.Client(timeout=config["request_timeout"], follow_redirects=False,
                                   headers={"User-Agent": config["user_agent"]})
        self.robots = {}
        self.last_request = {}
        self.paused = set()
        self.pause_status = {}
        self.discovery_errors = []

    def close(self):
        self.client.close()

    def policy(self, url: str):
        url = canonical_url(url)
        host = urlsplit(url).hostname
        matches = [(key, row) for key, row in self.sources.items() if host in row["hosts"]]
        if len(matches) != 1:
            raise PermissionError(f"Unknown or ambiguous source: {host}")
        key, source = matches[0]
        if not source["allowed"]:
            raise PermissionError(f"Source disabled: {key}")
        # Validate resolved addresses too; never crawl loopback/private infrastructure.
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            raise PermissionError("Non-public address rejected")
        return key, source

    def _request(self, url: str, interval: float):
        host = urlsplit(url).hostname
        if host in self.paused:
            status = self.pause_status[host]
            raise PermissionError(f"{host}: requests paused after HTTP {status} for this run")
        retries = self.config.get("request_retries", 2)
        for attempt in range(retries + 1):
            wait = interval - (time.monotonic() - self.last_request.get(host, 0))
            if wait > 0:
                time.sleep(wait)
            self.last_request[host] = time.monotonic()
            try:
                with self.client.stream("GET", url) as response:
                    if response.status_code in {403, 429}:
                        self.paused.add(host)
                        self.pause_status[host] = response.status_code
                    if response.status_code >= 500 and attempt < retries:
                        time.sleep(2 ** attempt)
                        continue
                    if response.status_code >= 400:
                        response.raise_for_status()
                    body = bytearray()
                    for part in response.iter_bytes():
                        body.extend(part)
                        if len(body) > self.config["max_response_bytes"]:
                            raise ValueError("Response exceeds configured size limit")
                    return response.status_code, dict(response.headers), bytes(body)
            except httpx.TransportError:
                if attempt == retries:
                    raise
                time.sleep(2 ** attempt)

    def robot_policy(self, origin, interval):
        if origin in self.robots:
            return self.robots[origin]
        url = origin + "/robots.txt"
        for _ in range(4):
            self.policy(url)
            status, headers, body = self._request(url, interval)
            if 300 <= status < 400:
                target = canonical_url(urljoin(url, headers.get("location", "")))
                if urlsplit(target).path != "/robots.txt":
                    raise PermissionError("Unsafe robots.txt redirect")
                url = target
                continue
            if status != 200 or b"<html" in body[:2000].lower() or b"<!doctype html" in body[:2000].lower():
                raise PermissionError("robots.txt unavailable: fail closed")
            robot = RobotFileParser()
            robot.parse(body.decode("utf-8", errors="replace").splitlines())
            self.robots[origin] = robot
            return robot
        raise PermissionError("Too many robots.txt redirects")

    def fetch(self, url: str):
        for _ in range(5):
            url = canonical_url(url)
            key, source = self.policy(url)
            origin = "https://" + urlsplit(url).netloc
            robot = self.robot_policy(origin, source["min_interval_seconds"])
            if not robot.can_fetch(self.config["user_agent"], url):
                raise PermissionError(f"robots.txt disallows {url}")
            interval = max(source["min_interval_seconds"], robot.crawl_delay(self.config["user_agent"]) or 0)
            rate = robot.request_rate(self.config["user_agent"])
            if rate and rate.requests:
                interval = max(interval, rate.seconds / rate.requests)
            status, headers, body = self._request(url, interval)
            if 300 <= status < 400:
                url = urljoin(url, headers.get("location", ""))
                continue
            return {"url": url, "source_id": key, "source": source, "body": body, "headers": headers}
        raise ValueError("Too many redirects")

    def discover(self, source_id: str, limit: int):
        return [record["url"] for record in self.discover_records(source_id, limit)]

    def discover_records(self, source_id: str, limit: int, *, exclude_urls=None):
        if source_id not in self.sources:
            raise ValueError("Unknown source")
        source = self.sources[source_id]
        if not source["allowed"]:
            raise PermissionError(f"Source disabled: {source_id}")
        if limit <= 0:
            raise ValueError("Discovery limit must be positive")
        records, urls = [], set(exclude_urls or ())
        for feed in source["feeds"]:
            try:
                result = self.fetch(feed)
            except (httpx.HTTPError, OSError, ValueError, PermissionError) as exc:
                self.discovery_errors.append({"source_id": source_id, "url": feed, "stage": "discovery",
                                              "error": f"{type(exc).__name__}: {exc}"})
                continue
            parsed = feedparser.parse(result["body"])
            if parsed.bozo and not parsed.entries:
                raise ValueError("Invalid RSS/Atom feed")
            for entry in parsed.entries:
                if not entry.get("link"):
                    continue
                try:
                    url = canonical_url(entry.link)
                    key, _ = self.policy(url)
                except (PermissionError, ValueError, OSError):
                    continue
                if source.get("article_pattern") and not re.search(source["article_pattern"], urlsplit(url).path):
                    continue
                if key == source_id and url not in urls:
                    urls.add(url)
                    records.append({"url": url, "source_id": source_id, "discovery_endpoint": feed,
                                    "discovery_method": "rss", "title": entry.get("title", ""),
                                    "published_at": entry.get("published", ""),
                                    "rss_summary": entry.get("summary", "")})
                if len(records) >= limit:
                    return records
        if not records and self.discovery_errors:
            raise ValueError(f"No article URLs found for {source_id}; see discovery errors")
        return records


def katana_urls(path: Path):
    """Import discovery output only; page downloads still go through Access.fetch."""
    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line) if line.lstrip().startswith("{") else line.strip()
        url = row if isinstance(row, str) else row.get("request", {}).get("endpoint")
        if not url:
            raise ValueError("Expected Katana JSONL request.endpoint or one HTTPS URL per line")
        url = canonical_url(url)
        if url not in urls:
            urls.append(url)
    return urls
