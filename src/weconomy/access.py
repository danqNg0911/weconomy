"""One policy gate for feeds, pages and externally discovered URLs."""
import ipaddress
import json
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

    def close(self):
        self.client.close()

    def policy(self, url: str):
        url = canonical_url(url)
        host = urlsplit(url).hostname
        matches = [(key, row) for key, row in self.sources.items() if host in row["hosts"]]
        if len(matches) != 1:
            raise PermissionError(f"Unknown or ambiguous source: {host}")
        key, source = matches[0]
        if not source["allowed"] or not source.get("permission_basis"):
            raise PermissionError(f"Source disabled: {key}: {source.get('permission_basis')}")
        # Validate resolved addresses too; never crawl loopback/private infrastructure.
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            raise PermissionError("Non-public address rejected")
        return key, source

    def _request(self, url: str, interval: float):
        host = urlsplit(url).hostname
        wait = interval - (time.monotonic() - self.last_request.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        self.last_request[host] = time.monotonic()
        # No retry loop on 403/429. A later explicit run can retry after terms/access review.
        with self.client.stream("GET", url) as response:
            if response.status_code >= 400:
                response.raise_for_status()
            body = bytearray()
            for part in response.iter_bytes():
                body.extend(part)
                if len(body) > self.config["max_response_bytes"]:
                    raise ValueError("Response exceeds configured size limit")
            return response.status_code, dict(response.headers), bytes(body)

    def fetch(self, url: str):
        for _ in range(5):
            url = canonical_url(url)
            key, source = self.policy(url)
            origin = "https://" + urlsplit(url).netloc
            if origin not in self.robots:
                status, _, body = self._request(origin + "/robots.txt", source["min_interval_seconds"])
                if status != 200:
                    raise PermissionError("robots.txt unavailable: fail closed")
                robot = RobotFileParser()
                robot.parse(body.decode("utf-8", errors="replace").splitlines())
                self.robots[origin] = robot
            robot = self.robots[origin]
            if not robot.can_fetch(self.config["user_agent"], url):
                raise PermissionError(f"robots.txt disallows {url}")
            interval = max(source["min_interval_seconds"], robot.crawl_delay(self.config["user_agent"]) or 0)
            status, headers, body = self._request(url, interval)
            if 300 <= status < 400:
                url = urljoin(url, headers.get("location", ""))
                continue
            return {"url": url, "source_id": key, "source": source, "body": body, "headers": headers}
        raise ValueError("Too many redirects")

    def discover(self, source_id: str, limit: int):
        if source_id not in self.sources:
            raise ValueError("Unknown source")
        source = self.sources[source_id]
        if not source["allowed"]:
            raise PermissionError(f"Source disabled: {source_id}")
        urls = []
        for feed in source["feeds"]:
            result = self.fetch(feed)
            parsed = feedparser.parse(result["body"])
            if parsed.bozo and not parsed.entries:
                raise ValueError("Invalid RSS/Atom feed")
            for entry in parsed.entries:
                if not entry.get("link"):
                    continue
                url = canonical_url(entry.link)
                key, _ = self.policy(url)
                if key == source_id and url not in urls:
                    urls.append(url)
                if len(urls) >= limit:
                    return urls
        return urls


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
