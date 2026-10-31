"""Immutable runs: bronze source snapshots -> silver text/spans -> gold claims/events."""
import hashlib
import importlib.metadata
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pyarrow as pa
import pyarrow.parquet as pq
import trafilatura
import yaml

from .access import Access, canonical_url
from .nlp import NLP, extract_relations, normalize, route, sentences
from .schema import SCHEMA_VERSION, SCHEMAS, stable_id


def now():
    return datetime.now(timezone.utc).isoformat()


def load_config(path):
    path = Path(path).resolve()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    root = path.parent.parent
    for key in ("aliases", "sources", "output"):
        config[key] = str((root / config[key]).resolve())
    if config["max_documents"] <= 0 or not 0 <= config["near_duplicate_threshold"] <= 1:
        raise ValueError("Invalid document limit or duplicate threshold")
    return config


def read_table(run, name):
    layer = "bronze" if name == "bronze" else "gold" if name in {"entities", "relations", "events"} else "silver"
    return pq.read_table(Path(run) / layer / f"{name}.parquet").to_pylist()


def shingles(text):
    tokens = re.findall(r"\w+", text.casefold())
    return {tuple(tokens[i:i+5]) for i in range(max(1, len(tokens) - 4))}


def process(config, *, manifest=None, urls=None):
    nlp = NLP(config)
    run = Path(config["output"]) / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid4().hex[:8])
    run.mkdir(parents=True, exist_ok=False)
    tables = {key: [] for key in SCHEMAS}
    errors, seen_urls, seen_text = [], set(), []
    access = Access(config)
    entities, events, claim_ids = {}, {}, set()
    if manifest is not None:
        manifest = Path(manifest).resolve()
        items = json.loads(manifest.read_text(encoding="utf-8"))["documents"]
        if len(items) > config["max_documents"]:
            raise ValueError("Manifest exceeds document budget")
    else:
        items = [{"url": u} for u in (urls or [])][:config["max_documents"]]
    try:
        for item in items:
            try:
                url = canonical_url(item["url"])
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                if manifest is not None:
                    # Offline snapshots require explicit source provenance and a redistribution basis.
                    for key in ("source_id", "license", "attribution", "retrieved_at", "kind"):
                        if not item.get(key):
                            raise ValueError(f"Missing snapshot provenance: {key}")
                    local = (manifest.parent / item["path"]).resolve()
                    if not local.is_relative_to(manifest.parent):
                        raise ValueError("Snapshot path escapes manifest directory")
                    raw = local.read_bytes()
                    if metadata_hash := item.get("sha256"):
                        if hashlib.sha256(raw).hexdigest() != metadata_hash:
                            raise ValueError("Snapshot checksum mismatch")
                    if len(raw) > config["max_response_bytes"]:
                        raise ValueError("Snapshot too large")
                    metadata = item
                    headers = {}
                else:
                    fetched = access.fetch(url)
                    url, raw, headers = fetched["url"], fetched["body"], fetched["headers"]
                    if "text/html" not in headers.get("content-type", "").lower():
                        raise ValueError("Article response is not HTML")
                    source = fetched["source"]
                    metadata = dict(source, source_id=fetched["source_id"], retrieved_at=now(),
                                    attribution=f"Contributors: {url}; history: {url}?action=history",
                                    language_hint=source["language"])
                raw_hash = hashlib.sha256(raw).hexdigest()
                doc_id = stable_id(url, raw_hash)
                raw_html = raw.decode("utf-8", errors="replace")
                tables["bronze"].append({
                    "document_id": doc_id, "url": url, "source_id": metadata["source_id"],
                    "kind": metadata["kind"], "license": metadata["license"],
                    "attribution": metadata["attribution"], "retrieved_at": metadata["retrieved_at"],
                    "published_at": metadata.get("published_at", ""),
                    "language_hint": metadata.get("language_hint", ""), "raw_html": raw_html,
                    "raw_sha256": raw_hash, "response_headers": json.dumps(headers),
                })
                extracted = trafilatura.extract(raw_html, url=url, output_format="json", with_metadata=True,
                                                include_comments=False, include_tables=False, favor_precision=True)
                if not extracted:
                    raise ValueError("Trafilatura returned no article")
                extracted = json.loads(extracted)
                text = normalize(extracted.get("text", ""))
                if len(text) < config["min_text_chars"]:
                    raise ValueError("Extracted article too short")
                language, routing = route(text, metadata.get("language_hint", ""))
                digest = hashlib.sha256(text.casefold().encode()).hexdigest()
                sig, duplicate = shingles(text), ""
                for old_id, old_lang, old_hash, old_sig in seen_text:
                    if language == old_lang and (digest == old_hash or
                            len(sig & old_sig) / max(1, len(sig | old_sig)) >= config["near_duplicate_threshold"]):
                        duplicate = old_id
                        break
                tables["articles"].append({"document_id": doc_id, "title": extracted.get("title") or "",
                    "text": text, "language": language, "routing_method": routing,
                    "content_sha256": digest, "duplicate_of": duplicate})
                if duplicate:
                    continue
                seen_text.append((doc_id, language, digest, sig))
                for sentence in sentences(text):
                    sid = stable_id(doc_id, str(sentence["start"]), sentence["text"])
                    tables["sentences"].append(dict(sentence, sentence_id=sid, document_id=doc_id))
                    mentions = nlp.mentions(sentence["text"], language)
                    for mention in mentions:
                        entity = mention["entity"]
                        entities[entity["entity_id"]] = entity
                        start, end = sentence["start"] + mention["start"], sentence["start"] + mention["end"]
                        tables["mentions"].append({"mention_id": stable_id(sid, str(start), str(end)),
                            "document_id": doc_id, "sentence_id": sid, "entity_id": entity["entity_id"],
                            "entity_type": entity["entity_type"], "surface": mention["surface"],
                            "method": mention["method"], "start": start, "end": end})
                    for relation in extract_relations(sentence["text"], mentions, language):
                        # shortcut: unknown event dates deduplicate within document only. Never merge repeated
                        # investments/acquisitions across articles solely by the actor pair or publication date.
                        event_date = ""
                        eid = stable_id(relation["subject_id"], relation["predicate"], relation["object_id"],
                                        relation["assertion_status"], doc_id)
                        events[eid] = {"event_id": eid, "subject_id": relation["subject_id"],
                            "predicate": relation["predicate"], "object_id": relation["object_id"],
                            "assertion_status": relation["assertion_status"], "event_date": event_date,
                            "dedup_scope": "within_document_unknown_date"}
                        claim_id = stable_id(eid, sid)
                        if claim_id in claim_ids:
                            continue
                        claim_ids.add(claim_id)
                        tables["relations"].append(dict(relation, claim_id=claim_id, event_id=eid,
                            document_id=doc_id, sentence_id=sid, evidence=sentence["text"],
                            evidence_start=sentence["start"], evidence_end=sentence["end"],
                            review_status="unreviewed", event_date=event_date))
            except Exception as exc:
                # Retain per-document failures and continue; CLI returns nonzero if any failed.
                errors.append({"url": item.get("url"), "error": f"{type(exc).__name__}: {exc}"})
    finally:
        access.close()
    tables["entities"] = list(entities.values())
    tables["events"] = list(events.values())
    for name, rows in tables.items():
        layer = "bronze" if name == "bronze" else "gold" if name in {"entities", "events", "relations"} else "silver"
        folder = run / layer
        folder.mkdir(exist_ok=True)
        pq.write_table(pa.Table.from_pylist(rows, schema=SCHEMAS[name]), folder / f"{name}.parquet",
                       compression="zstd")
    report = {"schema_version": SCHEMA_VERSION, "created_at": now(), "config": config,
              "counts": {key: len(value) for key, value in tables.items()}, "errors": errors,
              "duplicate_documents": sum(bool(a["duplicate_of"]) for a in tables["articles"]),
              "relation_types_observed": sorted({r["predicate"] for r in tables["relations"]}),
              "quality": {"precision": None, "recall": None, "f1": None,
                          "reason": "Requires independently annotated held-out labels"},
              "targets": {"nodes": 2000, "edges": 5000, "relation_types": 10, "precision": 0.9},
              "packages": {p: importlib.metadata.version(p) for p in
                           ("weconomy", "trafilatura", "pyarrow", "feedparser", "networkx", "neo4j")},
              "status": "partial" if errors else "completed"}
    if config["ner_backend"] == "models":
        for package in ("spacy", "underthesea", config["english_model"]):
            report["packages"][package] = importlib.metadata.version(package)
    (run / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (run / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")
    # Preserve the exact alias/source policy alongside each immutable run.
    for key in ("aliases", "sources"):
        (run / f"{key}.yaml").write_bytes(Path(config[key]).read_bytes())
    return run, report
