"""Durable, resumable datasets built from immutable pipeline runs.

The catalog stores accepted pipeline rows as JSON in SQLite. Pipeline artifacts
remain immutable under ``batches/`` and are referenced by each accepted article.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import sqlite3
import time
from contextlib import closing, contextmanager
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

import pyarrow as pa
import pyarrow.parquet as pq
import yaml

from . import access, domain, extraction, nlp, pipeline, schema
from .access import Access, canonical_url
from .progress import heartbeat
from .quality import validate

_TABLES = ("articles", "bronze", "sentences", "mentions", "entities", "relations", "events")
_DB = "catalog.sqlite3"
_MERGE_ORDER = {"MERGED_WITH", "PARTNERED_WITH"}
_TERMINAL = {"accepted", "duplicate_url", "duplicate_content", "out_of_scope",
             "quarantined", "error", "policy_rejected"}


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash(value):
    return hashlib.sha256(value).hexdigest()


def _file_hash(path):
    p = Path(path)
    return _hash(p.read_bytes()) if p.is_file() else "missing"


def _code_hash():
    modules = (pipeline, extraction, nlp, schema, domain, access)
    return _hash(b"\n".join(Path(m.__file__).read_bytes() for m in modules))


def _processing_fingerprint(config):
    """Hash extraction/NLP inputs while allowing collection settings to vary."""
    collection_settings = {"output", "sources", "aliases", "version", "targets", "crawl",
                           "batch_size", "objectives", "max_articles", "max_documents",
                           "user_agent", "request_timeout", "request_retries", "max_response_bytes"}
    settings = {k: v for k, v in config.items()
                if k not in collection_settings}
    aliases = _file_hash(config.get("aliases", ""))
    packages = {}
    if config.get("ner_backend") == "models":
        try:
            packages["gliner"] = importlib.metadata.version("gliner")
        except importlib.metadata.PackageNotFoundError as exc:
            raise ValueError("Configured NLP backend requires package: gliner") from exc
    backend = {"nlp": getattr(nlp, "__version__", "configured"),
               "schema": schema.SCHEMA_VERSION,
               "extractor": getattr(pipeline, "EXTRACTOR_VERSION", "unknown"),
               "python": platform.python_version(), "packages": packages}
    for package in ("trafilatura", "lxml"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ValueError(f"Required extraction package is unavailable: {package}") from exc
    return _hash(_json({"settings": settings, "aliases": aliases, "backend": backend,
                        "domain": domain.DOMAIN_VERSION, "code": _code_hash()}).encode())


def validate_dataset_resume(config, dataset):
    """Fail before crawling when a requested catalog cannot be resumed safely."""
    db = Path(dataset) / _DB
    if not db.is_file():
        raise FileNotFoundError(db)
    with closing(sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
        row = conn.execute("SELECT value FROM meta WHERE key='processing_fingerprint'").fetchone()
    previous = json.loads(row[0]) if row else None
    if previous and previous != _processing_fingerprint(config):
        raise ValueError("Dataset processing fingerprint is incompatible")


def _connect(dataset):
    dataset = Path(dataset)
    dataset.mkdir(parents=True, exist_ok=True)
    db = dataset / _DB
    conn = sqlite3.connect(db, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS queue (
          url TEXT PRIMARY KEY, source TEXT NOT NULL, status TEXT NOT NULL,
          error TEXT, batch_id TEXT, allocated_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS batches (
          batch_id TEXT PRIMARY KEY, root TEXT NOT NULL, urls TEXT NOT NULL,
          status TEXT NOT NULL, run TEXT, created_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS replay_items (
          url TEXT PRIMARY KEY, archive_file TEXT NOT NULL, source_run TEXT NOT NULL,
          source_document_id TEXT NOT NULL, raw_sha256 TEXT NOT NULL, metadata TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS replay_archives (
          source_run TEXT PRIMARY KEY, signature TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS records (
          table_name TEXT NOT NULL, record_key TEXT NOT NULL, payload TEXT NOT NULL,
          PRIMARY KEY(table_name, record_key));
        CREATE INDEX IF NOT EXISTS records_article_url ON records
          (json_extract(payload,'$.canonical_url'))
          WHERE table_name='articles';
        CREATE INDEX IF NOT EXISTS records_article_hash ON records
          (json_extract(payload,'$.content_sha256'))
          WHERE table_name='articles';
    """)
    conn.commit()
    return conn


def _read_connect(dataset):
    db = (Path(dataset) / _DB).resolve()
    conn = sqlite3.connect(f"{db.as_uri()}?mode=ro", uri=True, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only=ON")
    conn.execute("BEGIN")
    return conn


@contextmanager
def _writer_lock(dataset):
    lock_path = Path(dataset) / ".writer.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            if lock.read(1) == b"":
                lock.seek(0)
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise RuntimeError(f"Another dataset writer holds {lock_path}") from exc
            try:
                yield
            finally:
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise RuntimeError(f"Another dataset writer holds {lock_path}") from exc
            try:
                yield
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _meta(conn, key, default=None):
    row = conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return json.loads(row[0]) if row else default


def _set_meta(conn, key, value):
    conn.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (key, _json(value)))


def _policy_result(client, url):
    try:
        source_id, source = client.policy(url)
    except PermissionError as exc:
        return None, str(exc) or "policy rejected"
    if not isinstance(source, dict):
        return None, "policy returned an invalid source"
    kind = str(source.get("kind", "")).casefold()
    if str(source_id).casefold() in {"wikinews_en", "wikinews", "encyclopedia"}:
        return None, "source is explicitly excluded"
    if kind != "news" or source.get("allowed") is not True:
        return None, "source is not allowed news"
    return source_id, None


def _classify(article):
    result = domain.classify(article.get("title") or "", article.get("text") or "",
                             article.get("language") or "")
    if isinstance(result, dict):
        return bool(result.get("in_scope")), result.get("reasons", []), result.get("scope")
    if isinstance(result, (tuple, list)):
        return bool(result[0]), result[1] if len(result) > 1 else [], result[2] if len(result) > 2 else None
    return bool(result), [], None


def _put(conn, table, key, value):
    payload = _json(value)
    row = conn.execute("SELECT payload FROM records WHERE table_name=? AND record_key=?",
                       (table, str(key))).fetchone()
    if row:
        if row[0] != payload:
            if table == "entities":
                old = json.loads(row[0])
                def normalize(item):
                    return {k: v.casefold() if k == "name" and isinstance(v, str) else v
                            for k, v in item.items()}
                if normalize(old) == normalize(value):
                    return
            raise ValueError(f"Conflicting {table} record ID: {key}")
        return
    conn.execute("INSERT INTO records(table_name,record_key,payload) VALUES(?,?,?)",
                 (table, str(key), payload))


def _rows(conn, table):
    return [json.loads(row[0]) for row in conn.execute(
        "SELECT payload FROM records WHERE table_name=? ORDER BY record_key", (table,))]


def _article_key(row):
    key = row.get("document_id")
    if not key:
        raise ValueError("Article is missing document_id")
    return key


def _targets_met(counts, targets):
    provided = {key: value for key, value in targets.items() if value is not None}
    return bool(provided) and all(counts[key] >= value for key, value in provided.items())


def _ingest(conn, run, batch_id, requested_urls=(), replay_provenance=None):
    """Validate a complete immutable run and atomically add its accepted rows."""
    report = validate(run)
    if not report.get("valid"):
        raise ValueError(f"Pipeline run failed validation: {run}")
    tables = {name: pipeline.read_table(run, name) for name in _TABLES}
    entities = {r["entity_id"]: r for r in tables["entities"] if r.get("entity_id")}
    manifest = json.loads((Path(run) / "manifest.json").read_text(encoding="utf-8"))
    requested_by_doc = manifest.get("requested_urls_by_document", {})
    bronze_sources = {r.get("document_id"): r.get("source_id") for r in tables["bronze"]
                      if r.get("document_id")}
    articles = {r["document_id"]: r for r in tables["articles"]}
    accepted_ids = set()
    replay_provenance = replay_provenance or {}
    decisions = {canonical_url(u): "error" for u in requested_urls}
    original_urls = {canonical_url(u): canonical_url(u) for u in requested_urls}
    for doc_id, article in articles.items():
        final = canonical_url(article.get("canonical_url") or "")
        input_urls = requested_by_doc.get(doc_id, [])
        input_urls = [input_urls] if isinstance(input_urls, str) else input_urls
        original = ((input_urls[0] if input_urls else None) or article.get("source_url")
                    or article.get("original_url") or article.get("url"))
        if original:
            original_urls[canonical_url(original)] = final
        request_keys = [canonical_url(u) for u in input_urls] or [canonical_url(original) if original else final]
        for request_key in request_keys:
            original_urls[request_key] = final

        def decide(value):
            for request_key in request_keys:
                decisions[request_key] = value

        if article.get("duplicate_of"):
            decide("duplicate_url")
            continue
        if article.get("content_status") != "body_checked" or not article.get("nlp_eligible"):
            decide("quarantined")
            continue
        in_scope, reasons, scope = _classify(article)
        article.update(domain_in_scope=in_scope, domain_reasons=reasons, domain_scope=scope)
        if not in_scope:
            decide("out_of_scope")
            continue
        url = canonical_url(article.get("canonical_url") or "")
        existing = conn.execute("SELECT record_key FROM records WHERE table_name='articles' AND "
                                "json_extract(payload,'$.canonical_url')=?", (url,)).fetchone()
        existing_hash = conn.execute("SELECT record_key FROM records WHERE table_name='articles' AND "
                                     "json_extract(payload,'$.content_sha256')=?",
                                     (article.get("content_sha256"),)).fetchone()
        if existing or existing_hash:
            decide("duplicate_url" if existing else "duplicate_content")
            continue
        article["source_run"] = str(run)
        if doc_id in replay_provenance:
            article.update(replay_provenance[doc_id])
        _put(conn, "articles", _article_key(article), article)
        accepted_ids.add(doc_id)
        decide("accepted")
    accepted_entity_ids = set()
    for row in tables["mentions"]:
        if row.get("document_id") in accepted_ids and row.get("entity_id"):
            accepted_entity_ids.add(row["entity_id"])
    for row in tables["relations"]:
        if row.get("document_id") in accepted_ids:
            accepted_entity_ids.update(x for x in (row.get("subject_id"), row.get("object_id")) if x)
    for entity_id in accepted_entity_ids:
        row = entities.get(entity_id)
        if row:
            _put(conn, "entities", entity_id, row)
    for name in ("bronze", "sentences", "mentions", "entities", "relations", "events"):
        for row in tables[name]:
            doc_id = row.get("document_id")
            if doc_id and doc_id not in accepted_ids:
                continue
            if name == "entities":
                continue
            if name == "events":
                if not row.get("event_id"):
                    continue
                evidence = [c for c in tables["relations"]
                            if c.get("event_id") == row["event_id"]
                            and c.get("document_id") in accepted_ids]
                if not evidence:
                    continue
                by_document = {}
                for claim in evidence:
                    by_document.setdefault(claim["document_id"], []).append(claim["claim_id"])
                for evidence_doc, claim_ids in by_document.items():
                    event = dict(row, document_id=evidence_doc, source_claim_ids=sorted(claim_ids))
                    _put(conn, "events", f"{row['event_id']}:{evidence_doc}", event)
                continue
            if name == "relations":
                if row.get("subject_id") not in entities or row.get("object_id") not in entities:
                    continue
                if not row.get("claim_id") or not row.get("sentence_id"):
                    raise ValueError("Claim is missing claim_id or sentence_id")
                row = dict(row)
                row["original_subject_id"] = row.get("subject_id")
                row["original_object_id"] = row.get("object_id")
                if row.get("predicate") in _MERGE_ORDER and row["subject_id"] > row["object_id"]:
                    row = dict(row, subject_id=row["object_id"], object_id=row["subject_id"])
                row["source_run"] = str(run)
                row["source_document_id"] = row.get("document_id")
                row["source_id"] = bronze_sources.get(row.get("document_id"))
                _put(conn, name, row["claim_id"], row)
            elif name == "bronze":
                # Raw bytes/HTML remain in the immutable run; retain provenance only.
                if not row.get("document_id"):
                    raise ValueError("Bronze row is missing document_id")
                saved = {k: v for k, v in row.items() if k not in {"raw_bytes", "raw_html"}}
                if doc_id in replay_provenance:
                    saved.update(replay_provenance[doc_id])
                _put(conn, name, row["document_id"], saved)
            else:
                key_field = {"sentences": "sentence_id", "mentions": "mention_id"}[name]
                key = row.get(key_field)
                if not key:
                    raise ValueError(f"{name} row is missing {key_field}")
                _put(conn, name, key, row)
    for url in requested_urls:
        key = canonical_url(url)
        if key in decisions and decisions[key] == "error":
            # A redirect can change the document URL. The original queued URL
            # still receives the final document's actual ingestion decision.
            final = original_urls.get(key)
            decisions[key] = next((v for u, v in decisions.items()
                                   if original_urls.get(u) == final and v != "error"), "error")
    return decisions


def _recover(conn, dataset):
    """Ingest a completed pending run once; leave incomplete artifacts retryable."""
    pending = conn.execute("SELECT * FROM batches WHERE status='pending' ORDER BY created_at").fetchall()
    for batch in pending:
        root = Path(batch["root"])
        manifests = list(root.rglob("manifest.json")) if root.exists() else []
        if len(manifests) != 1:
            conn.execute("UPDATE batches SET status='interrupted' WHERE batch_id=?", (batch["batch_id"],))
            # Keep the consumed attempt charged; retrying allocates another attempt.
            conn.execute("UPDATE queue SET status='queued',batch_id=NULL,error='interrupted before manifest' WHERE batch_id=?",
                         (batch["batch_id"],))
            conn.commit()
            continue
        run = manifests[0].parent
        try:
            if not all((run / name).is_file() for name in ("config.yaml", "aliases.yaml", "sources.yaml")):
                raise ValueError("Pending run is missing its immutable processing snapshots")
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
            if manifest.get("status") not in {"completed", "partial"} or not validate(run).get("valid"):
                raise ValueError("Pending run is not complete and valid")
            urls = json.loads(batch["urls"])
            with conn:
                replay_file = root / "replay.json"
                provenance = {}
                if replay_file.is_file():
                    provenance = json.loads(replay_file.read_text(encoding="utf-8")).get("provenance", {})
                decisions = _ingest(conn, run, batch["batch_id"], urls, provenance)
                conn.execute("UPDATE batches SET status='committed',run=? WHERE batch_id=?",
                             (str(run), batch["batch_id"]))
                conn.executemany("UPDATE queue SET status=? WHERE url=?",
                                 [(decisions.get(canonical_url(u), "error"), u) for u in urls])
        except Exception as exc:
            conn.execute("UPDATE batches SET status='interrupted' WHERE batch_id=?", (batch["batch_id"],))
            conn.execute("UPDATE queue SET status='queued',error=? WHERE batch_id=?",
                         (str(exc), batch["batch_id"]))
            conn.commit()


_REPLAY_EXCLUDED = {"wikinews", "wikinews_en", "voa", "voice of america"}
_REPLAY_EXCLUDED_HOSTS = {"en.wikinews.org", "wikinews.org", "www.voanews.com", "voanews.com"}


def _replay_index(config, dataset, runs):
    """Validate eligible archived full-page bodies and stage each once, with bounded reads."""
    sources = yaml.safe_load(Path(config["sources"]).read_text(encoding="utf-8")) or {}
    sources = sources.get("sources", {})
    selected = {}
    archive_fingerprints = {}
    for raw_run in runs:
        run = Path(raw_run).resolve()
        manifest_path = run / "manifest.json"
        bronze_path = run / "bronze" / "bronze.parquet"
        articles_path = run / "silver" / "articles.parquet"
        if not (manifest_path.is_file() and bronze_path.is_file() and articles_path.is_file()):
            raise FileNotFoundError(f"Archive run is incomplete: {run}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") not in {"completed", "partial"}:
            raise ValueError(f"Archive run is not complete: {run}")
        eligible = set()
        for batch in pq.ParquetFile(articles_path).iter_batches(
                columns=["document_id", "content_status", "nlp_eligible", "duplicate_of", "quality_flags"],
                batch_size=512):
            for article in batch.to_pylist():
                flags = article.get("quality_flags") or "[]"
                try:
                    flags = json.loads(flags) if isinstance(flags, str) else flags
                except (TypeError, json.JSONDecodeError):
                    flags = []
                if (article.get("content_status") == "body_checked" and not article.get("duplicate_of")
                        and (article.get("nlp_eligible") or "nlp_processing_failed" in flags)):
                    eligible.add(article["document_id"])
        run_signature = []
        # Last run in explicit argument order wins for repeated URLs.
        for batch in pq.ParquetFile(bronze_path).iter_batches(batch_size=16):
            for row in batch.to_pylist():
                if row.get("document_id") not in eligible:
                    continue
                if row.get("capture_scope") != "full_page":
                    continue
                required = ("source_id", "attribution", "retrieved_at", "url", "raw_sha256")
                if any(not row.get(key) for key in required):
                    raise ValueError(f"Archive provenance is incomplete: {run}/{row.get('document_id')}")
                url = canonical_url(row["url"])
                raw = row.get("raw_bytes") or (row.get("raw_html") or "").encode("utf-8")
                if len(raw) > int(config["max_response_bytes"]):
                    raise ValueError(f"Archived body exceeds configured size limit: {run}/{row['document_id']}")
                digest = hashlib.sha256(raw).hexdigest()
                if digest != row["raw_sha256"]:
                    raise ValueError(f"Stored bronze checksum mismatch: {run}/{row['document_id']}")
                metadata = {key: value for key, value in row.items()
                            if key not in {"raw_bytes", "raw_html", "raw_path"}}
                run_signature.append((url, row["document_id"], digest, _hash(_json(metadata).encode())))
                host = urlsplit(url).hostname
                matching = [(name, source) for name, source in sources.items()
                            if host in source.get("hosts", [])]
                if (len(matching) != 1 or host in _REPLAY_EXCLUDED_HOSTS
                        or matching[0][0].casefold() in _REPLAY_EXCLUDED
                        or matching[0][1].get("kind", "").casefold() != "news"
                        or matching[0][1].get("allowed") is not True
                        or row.get("kind") != "news" or matching[0][0] != row["source_id"]):
                    continue
                source_key = _hash(_json([str(run), _hash(manifest_path.read_bytes())]).encode())[:20]
                archive_root = dataset / "replay_sources" / source_key
                archive_root.mkdir(parents=True, exist_ok=True)
                raw_file = archive_root / f"{row['document_id']}.bin"
                if raw_file.exists():
                    if _file_hash(raw_file) != digest:
                        raise ValueError(f"Staged archive body changed: {raw_file}")
                else:
                    temp_file = raw_file.with_suffix(".bin.tmp")
                    with temp_file.open("wb") as stream:
                        stream.write(raw)
                    temp_file.replace(raw_file)
                metadata["archive_raw_path"] = row.get("raw_path") or ""
                metadata["raw_path"] = f"bronze/html/{row['document_id']}.html"
                selected[url] = {"url": url, "archive_file": str(raw_file), "source_run": str(run),
                                 "source_document_id": row["document_id"], "raw_sha256": digest,
                                 "metadata": metadata}
        archive_fingerprints[str(run)] = _hash(_json({"manifest": _hash(manifest_path.read_bytes()),
                                                       "rows": sorted(run_signature)}).encode())
    return selected, archive_fingerprints


def _replay_policy_allows(config, url, source_id):
    """Check queued replay candidates against current policy without DNS or HTTP."""
    sources = yaml.safe_load(Path(config["sources"]).read_text(encoding="utf-8")) or {}
    sources = sources.get("sources", {})
    host = urlsplit(canonical_url(url)).hostname
    matching = [(name, source) for name, source in sources.items() if host in source.get("hosts", [])]
    return (len(matching) == 1 and host not in _REPLAY_EXCLUDED_HOSTS
            and matching[0][0] == source_id
            and matching[0][0].casefold() not in _REPLAY_EXCLUDED
            and matching[0][1].get("kind", "").casefold() == "news"
            and matching[0][1].get("allowed") is True)

def _stage_replay_batch(batch_root, replay_rows):
    """Create a small from_run-compatible immutable input and lineage sidecar."""
    input_root = batch_root / "input"
    (input_root / "bronze").mkdir(parents=True, exist_ok=True)
    rows, provenance = [], {}
    for item in replay_rows:
        raw = Path(item["archive_file"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["raw_sha256"]:
            raise ValueError(f"Staged archive checksum mismatch: {item['archive_file']}")
        row = dict(item["metadata"], raw_bytes=raw,
                   raw_html=raw.decode("utf-8", errors="replace"))
        rows.append(row)
        provenance[row["document_id"]] = {
            "archive_source_run": item["source_run"],
            "archive_source_document_id": item["source_document_id"],
            "archive_raw_sha256": item["raw_sha256"],
            "archive_raw_path": item["metadata"].get("archive_raw_path", ""),
        }
    parquet = input_root / "bronze" / "bronze.parquet"
    tmp_parquet = parquet.with_suffix(".parquet.tmp")
    pq.write_table(pa.Table.from_pylist(rows, schema=schema.SCHEMAS["bronze"]),
                   tmp_parquet, compression="zstd")
    tmp_parquet.replace(parquet)
    sidecar = batch_root / "replay.json"
    tmp_sidecar = sidecar.with_suffix(".json.tmp")
    tmp_sidecar.write_text(json.dumps({"source_runs": sorted({r["source_run"] for r in replay_rows}),
                                       "provenance": provenance}, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    tmp_sidecar.replace(sidecar)
    return input_root, provenance


def _graph_claims(conn):
    claims = _rows(conn, "relations")
    entities = _rows(conn, "entities")
    entity_types = {e.get("entity_id"): str(e.get("entity_type", e.get("type", ""))).upper()
                    for e in entities}
    valid_claims = []
    for row in claims:
        kinds = schema.RELATION_TYPES.get(row.get("predicate"))
        if (not kinds or (entity_types.get(row.get("subject_id")) in kinds[0]
                          and entity_types.get(row.get("object_id")) in kinds[1])):
            valid_claims.append(row)
    connected = {entity_id for r in valid_claims
                 for entity_id in (r["subject_id"], r["object_id"])}
    return valid_claims, connected


def _snapshot(conn):
    articles = _rows(conn, "articles")
    claims, connected = _graph_claims(conn)
    return {"articles": len(articles), "nodes": len(connected),
            "relations": len({(r.get("subject_id"), r.get("predicate"), r.get("object_id"))
                               for r in claims}),
            "claims": len(claims),
            "relation_types": len({r["predicate"] for r in claims})}


def _status(conn):
    counts = _snapshot(conn)
    queue = {row["status"]: row["n"] for row in conn.execute(
        "SELECT status,COUNT(*) n FROM queue GROUP BY status")}
    reason = _meta(conn, "reason", "inputs_exhausted")
    targets = _meta(conn, "targets")
    targets_met = _targets_met(counts, targets) if targets is not None else reason == "targets_met"
    return {"counts": counts, "queue": queue,
            "attempts_allocated": _meta(conn, "attempts_allocated", 0),
            "candidate_counts": _meta(conn, "candidate_counts", {}),
            "errors": _meta(conn, "errors", []),
            "error_history": _meta(conn, "error_history", []),
            "reason": reason, "targets_met": targets_met, "targets": targets,
            "remaining": ({k: max(0, v - counts.get(k, 0)) if v is not None else None
                           for k, v in targets.items()} if targets is not None else None),
            "scope": _meta(conn, "scope", "international business; domain heuristic"),
            "candidate_basis": _meta(conn, "candidate_basis", "explicit candidate input")}


def dataset_status(dataset: Path) -> dict:
    dataset = Path(dataset)
    if not (dataset / _DB).exists():
        return {"counts": {"articles": 0, "nodes": 0, "relations": 0, "claims": 0,
                            "relation_types": 0},
                "queue": {}, "attempts_allocated": 0, "candidate_counts": {}, "errors": [],
                "reason": "no_targets", "targets_met": False, "targets": None, "remaining": None,
                "scope": "international business; domain heuristic",
                "candidate_basis": "none"}
    with closing(_read_connect(dataset)) as conn:
        return _status(conn)


def collect_dataset(config, dataset: Path, *, urls: list[str] | None = None, articles: int | None = None,
                    nodes: int | None = None, relations: int | None = None,
                    relation_types: int | None = None, max_candidates: int = 1000,
                    batch_size: int = 20, resume: bool = False,
                    from_runs: list[Path] | None = None, progress=None) -> dict:
    """Collect explicitly supplied URLs or saved runs into a resumable dataset."""
    dataset = Path(dataset).resolve()
    targets = {"articles": articles, "nodes": nodes, "relations": relations,
               "relation_types": relation_types}
    if any(v is not None and v <= 0 for v in targets.values()):
        raise ValueError("Thresholds must be positive")
    if relation_types is not None and relation_types <= 0:
        raise ValueError("relation_types must be positive")
    if (max_candidates <= 0 or batch_size <= 0
            or sum(value is not None for value in (urls, from_runs)) != 1
            or (from_runs is not None and not from_runs)):
        raise ValueError("Invalid candidate budget, batch size, or input selection")
    with _writer_lock(dataset):
        existed = (dataset / _DB).exists()
        if existed and not resume:
            raise FileExistsError(f"Dataset already exists: {dataset}; use resume=True")
        if resume and not existed:
            raise FileNotFoundError(dataset / _DB)
        conn = _connect(dataset)
        try:
            fingerprint = _processing_fingerprint(config)
            previous = _meta(conn, "processing_fingerprint")
            if previous and previous != fingerprint:
                raise ValueError("Dataset processing fingerprint is incompatible")
            if not previous:
                _set_meta(conn, "processing_fingerprint", fingerprint)
            replay_items, replay_signatures = ({}, {})
            if from_runs is not None:
                replay_items, replay_signatures = _replay_index(config, dataset, from_runs)
                for source_run, signature in replay_signatures.items():
                    previous = conn.execute("SELECT signature FROM replay_archives WHERE source_run=?",
                                            (source_run,)).fetchone()
                    if previous and previous[0] != signature:
                        raise ValueError(f"Replay archive changed since it was registered: {source_run}")
                    conn.execute("INSERT OR IGNORE INTO replay_archives VALUES(?,?)",
                                 (source_run, signature))
            rejected_batches = set()
            for item in conn.execute("SELECT r.url,r.batch_id FROM replay_items i "
                                     "JOIN queue r ON r.url=i.url WHERE r.status IN ('queued','pending')").fetchall():
                replay = conn.execute("SELECT metadata FROM replay_items WHERE url=?", (item["url"],)).fetchone()
                source_id = json.loads(replay[0]).get("source_id")
                if not _replay_policy_allows(config, item["url"], source_id):
                    conn.execute("UPDATE queue SET status='policy_rejected',error='current source policy rejected replay' WHERE url=?",
                                 (item["url"],))
                    if item["batch_id"]:
                        rejected_batches.add(item["batch_id"])
            for batch_id in rejected_batches:
                conn.execute("UPDATE batches SET status='interrupted' WHERE batch_id=?", (batch_id,))
                conn.execute("UPDATE queue SET status='queued',batch_id=NULL WHERE batch_id=? AND status='pending'",
                             (batch_id,))
            conn.commit()
            _recover(conn, dataset)
            if resume:
                retry_rows = conn.execute("SELECT url,batch_id FROM queue WHERE status='error'").fetchall()
                if retry_rows:
                    retry_urls = {row["url"] for row in retry_rows}
                    retry_batches = {row["batch_id"] for row in retry_rows if row["batch_id"]}
                    errors = _meta(conn, "errors", [])
                    resolved = [e for e in errors if e.get("url") in retry_urls
                                or e.get("batch") in retry_batches]
                    _set_meta(conn, "error_history", [*_meta(conn, "error_history", []), *resolved])
                    _set_meta(conn, "errors", [e for e in errors if e not in resolved])
                    conn.execute("UPDATE queue SET status='queued',batch_id=NULL,error=NULL WHERE status='error'")
                    conn.commit()
            # Load models before allocation and reuse them across the invocation.
            if progress:
                progress({"event": "models_loading"})
            with heartbeat(progress, "Đang khởi tạo mô hình NLP"):
                nlp_engine = nlp.NLP(config)
            invocation = {"urls": urls,
                          "from_runs": [str(Path(p).resolve()) for p in from_runs] if from_runs else None}
            _set_meta(conn, "last_invocation", invocation)
            _set_meta(conn, "targets", targets)
            _set_meta(conn, "reason", "running")
            conn.commit()
            existing_urls = {canonical_url(r.get("canonical_url") or "") for r in _rows(conn, "articles")}
            existing_urls.update(row[0] for row in conn.execute("SELECT url FROM queue"))
            candidates = []
            candidate_counts = {}
            errors = _meta(conn, "errors", [])
            if from_runs is not None:
                for url, item in replay_items.items():
                    if url in existing_urls:
                        continue
                    candidates.append((url, item["metadata"]["source_id"]))
                candidate_counts["replay_candidates"] = len(replay_items)
                basis = "eligible full-page bodies replayed from immutable local runs"
            else:
                client = Access(config)
            try:
                if from_runs is None and urls is not None:
                    for raw in urls:
                        url = canonical_url(raw)
                        source_id, reason = _policy_result(client, url)
                        if reason:
                            errors.append({"url": url, "error": reason})
                            continue
                        candidates.append((url, source_id))
                    basis = "explicit URLs passing current source policy"
                unique_candidates = {}
                for candidate_url, candidate_source in candidates:
                    if candidate_url in existing_urls:
                        continue
                    unique_candidates.setdefault(candidate_url, candidate_source)
                candidates = list(unique_candidates.items())[:max_candidates]
            finally:
                if from_runs is None:
                    client.close()
            source_hash = _hash(_json({"urls": urls,
                                       "replay_signatures": replay_signatures,
                                       "source_file": _file_hash(config.get("sources", ""))}).encode())
            _set_meta(conn, "source_policy_hash", source_hash)
            _set_meta(conn, "candidate_counts", candidate_counts)
            _set_meta(conn, "candidate_basis", basis)
            _set_meta(conn, "errors", errors)
            for url, source in candidates:
                if url in existing_urls or conn.execute("SELECT 1 FROM queue WHERE url=?", (url,)).fetchone():
                    continue
                # Explicit article URLs were checked against the current source policy.
                conn.execute("INSERT INTO queue VALUES(?,?,?,?,?,?)",
                             (url, source, "queued", None, None, time.time()))
                if from_runs is not None:
                    item = replay_items[url]
                    conn.execute("INSERT INTO replay_items VALUES(?,?,?,?,?,?)",
                                 (url, item["archive_file"], item["source_run"],
                                  item["source_document_id"], item["raw_sha256"],
                                  _json(item["metadata"])))
            _set_meta(conn, "errors", errors)
            conn.commit()
            max_documents = int(config["max_documents"])
            if max_documents <= 0:
                raise ValueError("config.max_documents must be positive")
            budget = max_candidates
            allocated = int(_meta(conn, "attempts_allocated", 0))
            while allocated < budget:
                counts = _snapshot(conn)
                if _targets_met(counts, targets):
                    _set_meta(conn, "reason", "targets_met")
                    break
                slots = min(batch_size, max_documents, budget - allocated)
                replay_filter = ("AND EXISTS (SELECT 1 FROM replay_items i WHERE i.url=queue.url)"
                                 if from_runs is not None else
                                 "AND NOT EXISTS (SELECT 1 FROM replay_items i WHERE i.url=queue.url)")
                rows = conn.execute(f"SELECT * FROM queue WHERE status='queued' {replay_filter} "
                                    "ORDER BY allocated_at,url LIMIT ?",
                                    (slots,)).fetchall()
                if not rows:
                    _set_meta(conn, "reason", "inputs_exhausted")
                    break
                while True:
                    batch_id = uuid4().hex
                    batch_root = dataset / "batches" / batch_id
                    try:
                        batch_root.mkdir(parents=True, exist_ok=False)
                        break
                    except FileExistsError:
                        continue
                chosen = [row["url"] for row in rows]
                if progress:
                    progress({"event": "dataset_batch_start", "size": len(chosen),
                              "allocated": allocated, "budget": budget})
                with conn:
                    conn.execute("INSERT INTO batches VALUES(?,?,?,?,?,?)",
                                 (batch_id, str(batch_root), _json(chosen), "pending", None, time.time()))
                    conn.executemany("UPDATE queue SET status='pending',batch_id=? WHERE url=?",
                                     [(batch_id, url) for url in chosen])
                    allocated += len(chosen)
                    _set_meta(conn, "attempts_allocated", allocated)
                batch_config = dict(config, output=str(batch_root), max_documents=min(batch_size, max_documents))
                try:
                    replay_provenance = {}
                    if from_runs is not None:
                        replay_rows = []
                        for url in chosen:
                            item = conn.execute("SELECT * FROM replay_items WHERE url=?", (url,)).fetchone()
                            if not item:
                                raise ValueError(f"Missing immutable replay input for {url}")
                            replay_rows.append({**dict(item), "metadata": json.loads(item["metadata"])})
                        staged_run, replay_provenance = _stage_replay_batch(batch_root, replay_rows)
                        process_progress = (lambda event: progress({**event, "stage": "dataset"})) if progress else None
                        with heartbeat(progress, f"Đang chạy NLP cho batch dataset, {len(chosen)} bài"):
                            run, manifest = pipeline.process(batch_config, from_run=staged_run,
                                                             nlp_engine=nlp_engine, progress=process_progress)
                    else:
                        process_progress = (lambda event: progress({**event, "stage": "dataset"})) if progress else None
                        with heartbeat(progress, f"Đang tải và chạy NLP cho batch dataset, {len(chosen)} bài"):
                            run, manifest = pipeline.process(batch_config, urls=chosen, nlp_engine=nlp_engine,
                                                             progress=process_progress)
                    if not isinstance(manifest, dict):
                        manifest = {}
                    if manifest.get("status") not in {"completed", "partial"}:
                        raise RuntimeError(f"Pipeline run did not complete: {manifest.get('status')}")
                    with conn:
                        decisions = _ingest(conn, run, batch_id, chosen, replay_provenance)
                        conn.execute("UPDATE batches SET status='committed',run=? WHERE batch_id=?",
                                     (str(run), batch_id))
                        conn.executemany("UPDATE queue SET status=?,error=NULL WHERE url=?",
                                         [(decisions.get(canonical_url(u), "error"), u) for u in chosen])
                        _set_meta(conn, "last_run_errors", manifest.get("errors", []))
                        if manifest.get("errors"):
                            errors.extend({"batch": batch_id, **e} if isinstance(e, dict)
                                          else {"batch": batch_id, "error": str(e)}
                                          for e in manifest["errors"])
                        _set_meta(conn, "errors", errors)
                    counts = _snapshot(conn)
                    if progress:
                        progress({"event": "dataset_batch_done", "size": len(chosen), "counts": counts})
                    if _targets_met(counts, targets):
                        _set_meta(conn, "reason", "targets_met")
                        conn.commit()
                        break
                except Exception as exc:
                    error = {"batch": batch_id, "urls": chosen,
                             "error_type": type(exc).__name__, "error": str(exc)}
                    errors.append(error)
                    with conn:
                        conn.executemany("UPDATE queue SET status='error',error=?,batch_id=? WHERE url=?",
                                         [(str(exc), batch_id, url) for url in chosen])
                        conn.execute("UPDATE batches SET status='failed' WHERE batch_id=?", (batch_id,))
                        _set_meta(conn, "errors", errors)
                        _set_meta(conn, "reason", "error")
                    if progress:
                        progress({"event": "error", "stage": "dataset", **error})
                    continue
            else:
                _set_meta(conn, "reason", "budget_exhausted")
            counts = _snapshot(conn)
            if _targets_met(counts, targets):
                _set_meta(conn, "reason", "targets_met")
            elif allocated >= budget:
                _set_meta(conn, "reason", "budget_exhausted")
            conn.commit()
            result = _status(conn)
            result["batch_overshoot"] = max(0, result["counts"]["articles"] - articles) if articles else 0
            return result
        except Exception:
            with conn:
                if _meta(conn, "reason") == "running":
                    _set_meta(conn, "reason", "error")
            raise
        finally:
            conn.close()


def export_dataset(dataset: Path, output: Path) -> dict:
    """Export only committed catalog records to a new directory as JSON Lines."""
    dataset, output = Path(dataset), Path(output)
    if output.exists():
        raise FileExistsError(output)
    if not (dataset / _DB).exists():
        raise FileNotFoundError(dataset / _DB)
    output.mkdir(parents=True)
    with _writer_lock(dataset), closing(_connect(dataset)) as conn:
        status = _status(conn)
        for name in ("articles", "entities", "relations"):
            rows = _rows(conn, name)
            if name == "entities":
                _, connected = _graph_claims(conn)
                rows = [row for row in rows if row.get("entity_id") in connected]
            if name == "relations":
                rows, _ = _graph_claims(conn)
                unique = {}
                for row in rows:
                    key = (row.get("subject_id"), row.get("predicate"), row.get("object_id"))
                    unique.setdefault(key, row)
                rows = list(unique.values())
            (output / f"{name}.jsonl").write_text(
                "".join(_json(row) + "\n" for row in rows), encoding="utf-8")
        claims = _rows(conn, "relations")
        (output / "claims.jsonl").write_text(
            "".join(_json(row) + "\n" for row in claims), encoding="utf-8")
        manifest = {"status": status, "counts": status["counts"],
                    "quality": {"precision": None, "scope": status["scope"],
                                "candidate_basis": status["candidate_basis"]},
                    "source_runs": sorted({r.get("source_run") for r in [*claims, *_rows(conn, "articles")]
                                            if r.get("source_run")})}
        (output / "manifest.json").write_text(_json(manifest) + "\n", encoding="utf-8")
    return manifest
