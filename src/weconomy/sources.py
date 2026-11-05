"""Source inventory and an explicitly limited, one-article source probe."""
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import domain
from .access import Access
from .extraction import extract_article


def source_status(config, *, check=False, source_ids=None):
    sources = yaml.safe_load(Path(config["sources"]).read_text(encoding="utf-8"))["sources"]
    selected = list(source_ids) if source_ids is not None else list(sources)
    unknown = set(selected) - sources.keys()
    if unknown:
        raise KeyError(f"Unknown source id(s): {', '.join(sorted(unknown))}")

    rows = []
    for source_id in selected:
        source = sources[source_id]
        rows.append({
            "source_id": source_id,
            "enabled": bool(source.get("allowed", False)),
            "kind": source.get("kind"),
            "language": source.get("language"),
            "feeds": source.get("feeds", []),
            "terms_url": source.get("terms_url"),
            "excluded": source_id in {"wikinews_en", "techcrunch", "reuters", "bloomberg"}
            and not source.get("allowed", False),
        })

    report = {"sources": rows, "checked": bool(check),
              "warning": "One page probe only; this does not certify the whole source."}
    if not check:
        return report

    client = Access(config)
    try:
        for row in rows:
            if not row["enabled"] or row["kind"] != "news":
                continue
            row["checked_at"] = datetime.now(timezone.utc).isoformat()
            row["status"] = "unavailable"
            try:
                records = client.discover_records(row["source_id"], 1)
                if not records:
                    row["reason"] = "No article discovered"
                    continue
                record = records[0]
                row["discovery_endpoint"] = record.get("discovery_endpoint")
                row["candidate_url"] = record["url"]
                fetched = client.fetch(record["url"])
                row["candidate_url"] = fetched["url"]
                source = fetched["source"]
                body = fetched["body"]
                row["body_sha256"] = hashlib.sha256(body).hexdigest()
                extracted = extract_article(body, fetched["url"], source, config)
                scope = domain.classify(extracted["title"], extracted["text"], row["language"])
                in_scope = scope["in_scope"]
                eligible = extracted["content_status"] == "body_checked" and extracted["nlp_eligible"] and in_scope
                row.update({
                    "status": "out_of_scope" if not in_scope else "eligible" if eligible else "quarantined",
                    "content_status": extracted["content_status"],
                    "nlp_eligible": bool(extracted["nlp_eligible"]),
                    "chars": len(extracted["text"]),
                    "paragraphs": extracted["body_paragraphs"],
                    "coverage": extracted["trafilatura_coverage"],
                    "quality_flags": extracted["quality_flags"],
                    "in_scope": in_scope,
                    "scope_reasons": scope["reasons"],
                })
            except Exception as exc:
                row["error"] = f"{type(exc).__name__}: {exc}"
                errors = getattr(client, "discovery_errors", [])
                matching = [e for e in errors if e.get("source_id") == row["source_id"]]
                if matching:
                    row["discovery_errors"] = matching
                if getattr(client, "paused", set()) & set(sources[row["source_id"]].get("hosts", [])):
                    row["status"] = "blocked"
    finally:
        client.close()
    return report
