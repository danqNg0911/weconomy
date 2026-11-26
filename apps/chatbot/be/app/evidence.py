"""Indexed claim/document lookup. Build once from an export; never invent evidence."""

import argparse
import json
import sqlite3
from pathlib import Path

from .config import Settings


def edge_claim_ids(edge):
    ids = list(edge.get("claim_ids") or [])
    try:
        events = json.loads(edge.get("event_details_json") or "[]")
    except (ValueError, TypeError):
        events = []
    for event in events if isinstance(events, list) else []:
        if isinstance(event, dict):
            ids.extend(event.get("claim_ids") or [])
    return list(dict.fromkeys(value for value in ids if isinstance(value, str)))


def enrich(settings, details):
    graph = details["graph"]
    ids = list(dict.fromkeys(value for edge in graph["edges"] for value in edge.get("claim_ids", [])))
    path = Path(settings.evidence_index_path)
    if not ids:
        details["metadata"]["evidence_status"] = "ready" if graph["evidence"] else "missing_source"
        return details
    if not path.is_file():
        details["metadata"]["evidence_status"] = "missing_index"
        return details
    claims = {}
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as db:
        for offset in range(0, len(ids), 800):
            batch = ids[offset : offset + 800]
            rows = db.execute(
                "SELECT c.id,c.payload,d.payload FROM claims c LEFT JOIN documents d ON d.id=c.document_id "
                f"WHERE c.id IN ({','.join('?' for _ in batch)})",
                batch,
            )
            for identifier, claim_json, document_json in rows:
                claim = json.loads(claim_json)
                document = json.loads(document_json) if document_json else {}
                quote = claim.get("evidence")
                url = document.get("url") or document.get("canonical_url")
                if isinstance(quote, str) and quote.strip() and url:
                    claims[identifier] = (claim, document, url)
    existing = {item["id"]: item for item in graph["evidence"]}
    for edge in graph["edges"]:
        matches = [claims[value] for value in edge.get("claim_ids", []) if value in claims]
        matches.sort(
            key=lambda pair: (
                pair[0].get("review_status") != "manually_verified",
                pair[0].get("claim_id", ""),
            )
        )
        for claim, document, url in matches[:3]:
            identifier = f"{edge['id']}:{claim['claim_id']}"
            existing[identifier] = {
                "id": identifier,
                "targetType": "edge",
                "targetId": edge["id"],
                "claimId": claim["claim_id"],
                "quote": claim["evidence"],
                "title": document.get("title") or "",
                "url": url,
                "source": document.get("source_id") or "",
                "reviewStatus": claim.get("review_status") or "unreviewed",
                "assertionStatus": claim.get("assertion_status") or "reported",
                "trigger": claim.get("trigger") or "",
            }
    graph["evidence"] = list(existing.values())
    details["metadata"].update(
        evidence_status="ready" if len(claims) == len(ids) else "partial",
        evidence_claims_found=len(claims),
        evidence_claims_missing=len(ids) - len(claims),
    )
    return details


def read_rows(path):
    if path.suffix == ".jsonl":
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                if line.strip():
                    yield json.loads(line)
    else:
        try:
            import pyarrow.parquet as pq
        except ImportError as exc:
            raise RuntimeError("Install pyarrow to index Parquet exports: pip install pyarrow") from exc
        for batch in pq.ParquetFile(path).iter_batches():
            yield from batch.to_pylist()


def build_index(sources, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_files = []
    for source in sources:
        source = Path(source)
        source_files.extend(
            p
            for pattern in ("claims.jsonl", "articles.jsonl", "relations.parquet", "articles.parquet")
            for p in source.rglob(pattern)
            if "audit" not in p.relative_to(source).parts
        )
    if not source_files:
        raise ValueError("No claims/articles JSONL or relations/articles Parquet found")
    with sqlite3.connect(destination) as db:
        db.executescript(
            "CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY,payload TEXT NOT NULL);"
            "CREATE TABLE IF NOT EXISTS claims(id TEXT PRIMARY KEY,document_id TEXT,payload TEXT NOT NULL);"
        )
        for path in sorted(set(source_files)):
            claim = path.name in {"claims.jsonl", "relations.parquet"}
            for row in read_rows(path):
                key = row.get("claim_id" if claim else "document_id")
                if not key:
                    continue
                payload = json.dumps(row, ensure_ascii=False, default=str)
                if claim:
                    db.execute(
                        "INSERT OR REPLACE INTO claims VALUES(?,?,?)", (key, row.get("document_id"), payload)
                    )
                else:
                    db.execute("INSERT OR REPLACE INTO documents VALUES(?,?)", (key, payload))
        return {
            "claims": db.execute("SELECT count(*) FROM claims").fetchone()[0],
            "documents": db.execute("SELECT count(*) FROM documents").fetchone()[0],
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the local indexed evidence lookup")
    parser.add_argument("--source", type=Path, required=True, action="append")
    parser.add_argument("--output", type=Path, default=Path(Settings().evidence_index_path))
    args = parser.parse_args()
    print(json.dumps(build_index(args.source, args.output)))
