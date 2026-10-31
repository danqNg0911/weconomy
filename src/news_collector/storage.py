"""SQLite is authoritative; JSONL files are atomically rebuilt materialized views."""
import json
import os
import sqlite3
from collections import Counter
from pathlib import Path

from .models import Article, now


class Store:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(root / "crawler.db")
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
        PRAGMA journal_mode=WAL;
        PRAGMA foreign_keys=ON;
        CREATE TABLE IF NOT EXISTS sources(source_id TEXT PRIMARY KEY, config TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS discovery_endpoints(url TEXT PRIMARY KEY, source_id TEXT, evidence TEXT);
        CREATE TABLE IF NOT EXISTS url_queue(
          url TEXT PRIMARY KEY, source_id TEXT NOT NULL, status TEXT DEFAULT 'pending',
          metadata TEXT, discovered_at TEXT, last_attempt_at TEXT, retry_count INTEGER DEFAULT 0,
          next_retry_at TEXT, http_status INTEGER, last_error TEXT, duplicate_of TEXT);
        CREATE TABLE IF NOT EXISTS url_discoveries(url TEXT, endpoint TEXT, method TEXT,
          discovered_at TEXT, PRIMARY KEY(url, endpoint));
        CREATE TABLE IF NOT EXISTS articles(article_id TEXT PRIMARY KEY, source_id TEXT,
          canonical_url TEXT UNIQUE, content_hash TEXT UNIQUE, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS crawl_runs(run_id TEXT PRIMARY KEY, started_at TEXT,
          finished_at TEXT, status TEXT, report TEXT);
        CREATE TABLE IF NOT EXISTS crawl_errors(id INTEGER PRIMARY KEY, run_id TEXT, url TEXT,
          error_type TEXT, message TEXT, created_at TEXT);
        CREATE INDEX IF NOT EXISTS queue_source_status ON url_queue(source_id, status);
        CREATE INDEX IF NOT EXISTS article_source ON articles(source_id);
        ''')
        # Single-process writer: an interrupted fetch is safe to retry.
        with self.db:
            self.db.execute("UPDATE url_queue SET status='pending' WHERE status='fetching'")
            self.db.execute("UPDATE crawl_runs SET status='interrupted' WHERE status='running'")
        self.export()

    def enqueue(self, source: str, entries: list[dict]) -> int:
        count = 0
        with self.db:
            for item in entries:
                count += self.db.execute("INSERT OR IGNORE INTO url_queue(url,source_id,metadata,discovered_at) VALUES(?,?,?,?)",
                                         (item["url"], source, json.dumps(item, ensure_ascii=False), now())).rowcount
                self.db.execute("INSERT OR IGNORE INTO url_discoveries VALUES(?,?,?,?)",
                                (item["url"], item["endpoint"], item["method"], now()))
        return count

    def count(self, source: str) -> int:
        return self.db.execute("SELECT count(*) FROM articles WHERE source_id=?", (source,)).fetchone()[0]

    def state(self, url: str, status: str, error=None, http_status=None, retry_at=None, duplicate_of=None):
        with self.db:
            self.db.execute('''UPDATE url_queue SET status=?,last_error=?,http_status=?,next_retry_at=?,
                               duplicate_of=?,last_attempt_at=?,retry_count=retry_count+? WHERE url=?''',
                            (status, error, http_status, retry_at, duplicate_of, now(), int(status == "fetching"), url))

    def save(self, article: Article, queue_url: str) -> bool:
        with self.db:
            duplicate = self.db.execute("SELECT article_id FROM articles WHERE canonical_url=? OR content_hash=?",
                                        (str(article.canonical_url), article.content_hash)).fetchone()
            if duplicate:
                self.db.execute("UPDATE url_queue SET status='duplicate', duplicate_of=?,http_status=200 WHERE url=?",
                                (duplicate[0], queue_url))
                return False
            self.db.execute("INSERT INTO articles VALUES(?,?,?,?,?)", (article.article_id, article.source,
                            str(article.canonical_url), article.content_hash, article.model_dump_json()))
            self.db.execute("UPDATE url_queue SET status='success',http_status=200 WHERE url=?", (queue_url,))
        return True

    def export(self) -> Path:
        rows = list(self.db.execute("SELECT payload FROM articles ORDER BY source_id,article_id"))
        groups: dict[Path, list[str]] = {self.root / "exports" / "articles.jsonl": []}
        for row in rows:
            obj = json.loads(row[0])
            path = self.root / "raw" / obj["source"] / (obj["collected_at"][:7] + ".jsonl")
            groups.setdefault(path, []).append(row[0])
            groups[self.root / "exports" / "articles.jsonl"].append(row[0])
        for path, values in groups.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            temp = path.with_suffix(".tmp")
            with temp.open("w", encoding="utf-8", newline="\n") as f:
                for value in values:
                    f.write(value + "\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp, path)
        return self.root / "exports" / "articles.jsonl"

    def stats(self) -> dict:
        result = {}
        for row in self.db.execute("SELECT source_id FROM sources ORDER BY source_id"):
            source = row[0]
            counts = dict(self.db.execute("SELECT status,count(*) FROM url_queue WHERE source_id=? GROUP BY status", (source,)))
            payloads = [json.loads(r[0]) for r in self.db.execute("SELECT payload FROM articles WHERE source_id=?", (source,))]
            result[source] = {"articles_saved": len(payloads), "queue": counts,
                              "missing_published_at": sum(p["published_at"] is None for p in payloads),
                              "relevant_articles": sum(p["relevance_status"] == "relevant" for p in payloads),
                              "articles_by_month": dict(Counter((p["published_at"] or "unknown")[:7] for p in payloads))}
        return result
