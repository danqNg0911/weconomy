"""Immutable runs: bronze source snapshots -> silver text/spans -> gold claims/events."""
import hashlib
import importlib.metadata
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pyarrow as pa
import pyarrow.parquet as pq
import yaml

from .access import Access, canonical_url
from .extraction import EXTRACTOR_VERSION, extract_article, utc_date
from .nlp import NLP, document_person_aliases, normalize, route, sentences
from .schema import RELATION_TYPES, SCHEMA_VERSION, SCHEMAS, stable_id


def now():
    return datetime.now(timezone.utc).isoformat()


def load_config(path):
    path = Path(path).resolve()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    root = path.parent.parent
    for key in ("aliases", "sources", "output"):
        config[key] = str((root / config[key]).resolve())
    if (config["max_documents"] <= 0 or not 0 <= config["near_duplicate_threshold"] <= 1
            or config.get("min_article_words", 100) <= 0 or not 0 <= config.get("request_retries", 2) <= 5):
        raise ValueError("Invalid document limit or duplicate threshold")
    return config


def read_table(run, name):
    layer = "bronze" if name == "bronze" else "gold" if name in {"entities", "relations", "events"} else "silver"
    return pq.read_table(Path(run) / layer / f"{name}.parquet").to_pylist()


def shingles(text):
    tokens = re.findall(r"\w+", text.casefold())
    return {tuple(tokens[i:i+5]) for i in range(max(1, len(tokens) - 4))}


def fulltext_snapshots(runs):
    """Select one accepted capture per URL. Explicit input order resolves revisions (last wins)."""
    selected = {}
    for run in runs:
        accepted = {a["document_id"] for a in read_table(run, "articles")
                    if a["content_status"] == "body_checked" and a["nlp_eligible"]}
        for row in read_table(run, "bronze"):
            if row["document_id"] not in accepted:
                continue
            raw = row.get("raw_bytes") or row["raw_html"].encode("utf-8")
            if hashlib.sha256(raw).hexdigest() != row["raw_sha256"]:
                raise ValueError(f"Stored bronze checksum mismatch in {run}")
            selected[canonical_url(row["url"])] = row
    return [selected[url] for url in sorted(selected)]


def process(config, *, manifest=None, urls=None, from_run=None, from_runs=None,
            nlp_engine=None, source_overrides=None, progress=None):
    if sum(value is not None for value in (manifest, urls, from_run, from_runs)) != 1:
        raise ValueError("Provide exactly one input: manifest, URLs, from_run or from_runs")
    if urls is not None and not urls:
        raise ValueError("Provide at least one article URL")
    if manifest is not None:
        manifest = Path(manifest).resolve()
        items = json.loads(manifest.read_text(encoding="utf-8"))["documents"]
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            raise ValueError("Manifest documents must be a list of objects")
    elif from_run is not None:
        items = read_table(from_run, "bronze")
    elif from_runs is not None:
        if not from_runs:
            raise ValueError("Provide at least one run to merge")
        items = fulltext_snapshots(from_runs)
        if not items:
            raise ValueError("No accepted full-text captures to merge")
    else:
        items = [{"url": u} for u in urls]
    if len(items) > config["max_documents"]:
        raise ValueError("Input exceeds the configured document budget")
    # Invalid local inputs must not allocate a model/client or leave an orphan latest-run directory.
    nlp = nlp_engine if nlp_engine is not None else NLP(config)
    access = Access(config)
    if source_overrides:
        for source_id, override in source_overrides.items():
            if source_id not in access.sources:
                access.close()
                raise ValueError(f"Unknown source for article extraction: {source_id}")
            access.sources[source_id].update(override)
    output = Path(config["output"])
    try:
        while True:
            run = output / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid4().hex[:8])
            try:
                run.mkdir(parents=True, exist_ok=False)
                break
            except FileExistsError:
                continue
    except OSError:
        access.close()
        raise
    tables = {key: [] for key in SCHEMAS}
    errors, seen_urls, seen_documents, seen_text = [], set(), set(), []
    entities, events, claim_ids = {}, {}, set()
    requested_urls = {}
    try:
        for index, item in enumerate(items, 1):
            article = None
            current_url = item.get("url", "")
            title, entity_count, relation_count = "", 0, 0
            if progress:
                progress({"event": "article_start", "index": index, "total": len(items),
                          "url": current_url})
            try:
                url = canonical_url(item["url"])
                if url in seen_urls:
                    if progress:
                        progress({"event": "article_done", "index": index, "total": len(items),
                                  "url": url, "status": "duplicate_url"})
                    continue
                seen_urls.add(url)
                if from_run is not None or from_runs is not None:
                    raw = item.get("raw_bytes") or item["raw_html"].encode("utf-8")
                    if hashlib.sha256(raw).hexdigest() != item["raw_sha256"]:
                        raise ValueError("Stored bronze checksum mismatch")
                    metadata, headers = item, json.loads(item["response_headers"])
                    scope = item.get("capture_scope", "unknown")
                elif manifest is not None:
                    # Offline snapshots require explicit source provenance and a redistribution basis.
                    for key in ("source_id", "attribution", "retrieved_at", "kind"):
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
                    scope = item.get("capture_scope") or (
                        "excerpt" if "excerpt" in item.get("capture_method", "").lower() else "unknown")
                else:
                    fetched = access.fetch(url)
                    url, raw, headers = fetched["url"], fetched["body"], fetched["headers"]
                    if "text/html" not in headers.get("content-type", "").lower():
                        raise ValueError("Article response is not HTML")
                    source = fetched["source"]
                    source = {**source, **(source_overrides or {}).get(fetched["source_id"], {})}
                    metadata = dict(source, source_id=fetched["source_id"], retrieved_at=now(),
                                    attribution=f"{source.get('attribution', fetched['source_id'])}; {url}",
                                    language_hint=source["language"])
                    scope = "full_page"
                raw_hash = hashlib.sha256(raw).hexdigest()
                doc_id = stable_id(url, raw_hash)
                requested_urls.setdefault(doc_id, []).append(canonical_url(item["url"]))
                if doc_id in seen_documents:
                    if progress:
                        progress({"event": "article_done", "index": index, "total": len(items),
                                  "url": url, "status": "duplicate_document"})
                    continue
                seen_documents.add(doc_id)
                raw_html = raw.decode("utf-8", errors="replace")
                raw_path = f"bronze/html/{doc_id}.html"
                (run / "bronze/html").mkdir(parents=True, exist_ok=True)
                (run / raw_path).write_bytes(raw)
                tables["bronze"].append({
                    "document_id": doc_id, "url": url, "source_id": metadata["source_id"],
                    "kind": metadata["kind"], "attribution": metadata["attribution"],
                    "retrieved_at": metadata["retrieved_at"],
                    "published_at": metadata.get("published_at", ""),
                    "language_hint": metadata.get("language_hint", ""), "raw_html": raw_html,
                    "raw_sha256": raw_hash, "response_headers": json.dumps(headers),
                    "capture_scope": scope, "raw_bytes": raw, "raw_path": raw_path,
                    "discovery_endpoint": item.get("discovery_endpoint", ""),
                })
                source = access.sources.get(metadata["source_id"], {})
                extracted = extract_article(raw, url, source, config, capture_scope=scope)
                if scope == "unknown":
                    extracted.update(content_status="unknown", nlp_eligible=False)
                    extracted["quality_flags"].append("unknown_capture_scope")
                text = normalize(extracted["text"])
                if len(text) < config["min_text_chars"]:
                    extracted["nlp_eligible"] = False
                    extracted["quality_flags"].append("insufficient_text_chars")
                tables["bronze"][-1]["published_at"] = (extracted["published_at"]
                    or utc_date(metadata.get("published_at")) or utc_date(item.get("published_at")))
                language, routing = route(text, metadata.get("language_hint", ""))
                digest = hashlib.sha256(text.casefold().encode()).hexdigest()
                sig, duplicate = shingles(text), ""
                for old_id, old_lang, old_hash, old_sig in seen_text if extracted["nlp_eligible"] else []:
                    if language == old_lang and (digest == old_hash or
                            len(sig & old_sig) / max(1, len(sig | old_sig)) >= config["near_duplicate_threshold"]):
                        duplicate = old_id
                        break
                article = {"document_id": doc_id, "title": extracted.get("title") or "",
                    "text": text, "language": language, "routing_method": routing,
                    "content_sha256": digest, "duplicate_of": duplicate,
                    **{key: extracted[key] for key in ("canonical_url", "content_status", "extraction_method",
                       "extractor_version", "word_count", "body_paragraphs", "trafilatura_coverage",
                       "paragraph_coverage", "nlp_eligible")},
                    "published_at": tables["bronze"][-1]["published_at"],
                    "authors": json.dumps(extracted["authors"], ensure_ascii=False),
                    "quality_flags": json.dumps(extracted["quality_flags"], ensure_ascii=False)}
                tables["articles"].append(article)
                title = article["title"]
                if duplicate or not article["nlp_eligible"]:
                    if progress:
                        progress({"event": "article_done", "index": index, "total": len(items),
                                  "url": url, "status": "duplicate_content" if duplicate else article["content_status"],
                                  "title": title, "word_count": article["word_count"],
                                  "body_paragraphs": article["body_paragraphs"], "nlp_sentences": 0})
                    continue
                doc_sentences, doc_mentions, doc_relations = [], [], []
                doc_entities, doc_events = {}, {}
                for sentence in sentences(text):
                    sid = stable_id(doc_id, str(sentence["start"]), sentence["text"])
                    doc_sentences.append(dict(sentence, sentence_id=sid, document_id=doc_id))
                    mentions = nlp.mentions(sentence["text"], language)
                    for mention in mentions:
                        entity = mention["entity"]
                        doc_entities[entity["entity_id"]] = entity
                        start, end = sentence["start"] + mention["start"], sentence["start"] + mention["end"]
                        doc_mentions.append({"mention_id": stable_id(sid, str(start), str(end)),
                            "document_id": doc_id, "sentence_id": sid, "entity_id": entity["entity_id"],
                            "entity_type": entity["entity_type"], "surface": mention["surface"],
                            "method": mention["method"], "start": start, "end": end})
                    for relation in nlp.relations(sentence["text"], mentions, language):
                        doc_relations.append(dict(relation, document_id=doc_id, sentence_id=sid,
                            evidence=sentence["text"], evidence_start=sentence["start"],
                            evidence_end=sentence["end"], review_status="unreviewed", event_date=""))
                alias_map = document_person_aliases(doc_entities, doc_mentions)
                for mention in doc_mentions:
                    mention["entity_id"] = alias_map.get(mention["entity_id"], mention["entity_id"])
                    mention["entity_type"] = doc_entities[mention["entity_id"]]["entity_type"]
                doc_entities = {entity_id: entity for entity_id, entity in doc_entities.items()
                                if entity_id not in alias_map}
                resolved_relations = []
                for relation in doc_relations:
                    relation["subject_id"] = alias_map.get(relation["subject_id"], relation["subject_id"])
                    relation["object_id"] = alias_map.get(relation["object_id"], relation["object_id"])
                    if relation["subject_id"] == relation["object_id"]:
                        continue
                    constraints = RELATION_TYPES.get(relation["predicate"])
                    subject = doc_entities.get(relation["subject_id"])
                    object_ = doc_entities.get(relation["object_id"])
                    if (constraints and (not subject or not object_
                            or subject["entity_type"] not in constraints[0]
                            or object_["entity_type"] not in constraints[1])):
                        continue
                    # shortcut: unknown event dates deduplicate within document only.
                    eid = stable_id(relation["subject_id"], relation["predicate"], relation["object_id"],
                                    relation["assertion_status"], doc_id)
                    claim_id = stable_id(eid, relation["sentence_id"])
                    if claim_id in claim_ids:
                        continue
                    claim_ids.add(claim_id)
                    relation.update(event_id=eid, claim_id=claim_id)
                    resolved_relations.append(relation)
                    doc_events[eid] = {"event_id": eid, "subject_id": relation["subject_id"],
                        "predicate": relation["predicate"], "object_id": relation["object_id"],
                        "assertion_status": relation["assertion_status"], "event_date": relation["event_date"],
                        "dedup_scope": "within_document_unknown_date"}
                doc_relations = resolved_relations
                tables["sentences"].extend(doc_sentences)
                tables["mentions"].extend(doc_mentions)
                tables["relations"].extend(doc_relations)
                entities.update(doc_entities)
                events.update(doc_events)
                seen_text.append((doc_id, language, digest, sig))
                entity_count, relation_count = len(doc_entities), len(doc_relations)
                if progress:
                    progress({"event": "article_done", "index": index, "total": len(items),
                              "url": url, "status": article["content_status"], "title": title,
                              "word_count": article["word_count"],
                              "body_paragraphs": article["body_paragraphs"],
                              "nlp_sentences": len(doc_sentences),
                              "entities": entity_count, "relations": relation_count})
            except Exception as exc:
                # Retain per-document failures and continue; CLI returns nonzero if any failed.
                if article is not None:
                    article["nlp_eligible"] = False
                    flags = json.loads(article["quality_flags"])
                    article["quality_flags"] = json.dumps([*flags, "nlp_processing_failed"])
                errors.append({"url": item.get("url"), "error": f"{type(exc).__name__}: {exc}"})
                if progress:
                    progress({"event": "article_done", "index": index, "total": len(items),
                              "url": current_url, "status": "error", "error_type": type(exc).__name__,
                              "error": str(exc)})
    finally:
        access.close()
    tables["entities"] = list(entities.values())
    tables["events"] = list(events.values())
    quarantined = sum(not article["nlp_eligible"] for article in tables["articles"])
    for name, rows in tables.items():
        layer = "bronze" if name == "bronze" else "gold" if name in {"entities", "events", "relations"} else "silver"
        folder = run / layer
        folder.mkdir(exist_ok=True)
        pq.write_table(pa.Table.from_pylist(rows, schema=SCHEMAS[name]), folder / f"{name}.parquet",
                       compression="zstd")
    report = {"schema_version": SCHEMA_VERSION, "created_at": now(), "config": config,
              "counts": {key: len(value) for key, value in tables.items()}, "errors": errors,
              "duplicate_documents": sum(bool(a["duplicate_of"]) for a in tables["articles"]),
              "content_statuses": dict(Counter(a["content_status"] for a in tables["articles"])),
              "nlp_documents": sum(a["nlp_eligible"] and not a["duplicate_of"] for a in tables["articles"]),
              "quarantined_documents": quarantined, "extractor_version": EXTRACTOR_VERSION,
              "reprocessed_from": str(from_run) if from_run else None,
              "merged_from": [str(Path(p).resolve()) for p in (from_runs or [])],
              "requested_urls_by_document": requested_urls,
              "relation_types_observed": sorted({r["predicate"] for r in tables["relations"]}),
              "quality": {"precision": None, "recall": None, "f1": None,
                          "reason": "Requires independently annotated held-out labels"},
              "targets": {"nodes": 2000, "edges": 5000, "relation_types": 10, "precision": 0.9},
              "packages": {p: importlib.metadata.version(p) for p in
                           ("weconomy", "trafilatura", "pyarrow", "networkx", "neo4j")},
              "status": ("partial" if errors or quarantined
                         else "completed" if tables["articles"] else "no_new_documents")}
    if config["ner_backend"] == "models":
        report["packages"]["gliner"] = importlib.metadata.version("gliner")
    (run / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")
    # Preserve the exact alias/source policy alongside each immutable run.
    for key in ("aliases", "sources"):
        (run / f"{key}.yaml").write_bytes(Path(config[key]).read_bytes())
    # A manifest is the durable completion marker consumed by recovery.
    manifest_path = run / "manifest.json"
    manifest_path.with_suffix(".json.tmp").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path.with_suffix(".json.tmp").replace(manifest_path)
    return run, report
