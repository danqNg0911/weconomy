"""Build the public, text-free graph projection from a pinned normalized export."""
import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/normalized/international-business-v15-manual-20261112-global-business-only"
DESTINATION = ROOT / "public-data/v15-global-business-only-20261112"
PUBLIC_FIELDS = {
    "articles": {
        "document_id", "title", "canonical_url", "content_sha256", "content_status",
        "language", "published_at", "duplicate_of", "domain_scope", "domain_in_scope", "word_count",
    },
    "entities": {"entity_id", "name", "entity_type", "resolution_method", "domain_types"},
    "relations": {
        "claim_id", "event_id", "subject_id", "predicate", "object_id", "document_id", "sentence_id",
        "source_document_id", "source_id", "assertion_status", "review_status", "event_date", "rule_id",
        "normalization_source_object_id", "normalization_source_sentence_id", "normalization_source_subject_id",
        "original_object_id", "original_subject_id",
    },
    "claims": {
        "claim_id", "event_id", "subject_id", "predicate", "object_id", "document_id", "sentence_id",
        "source_document_id", "source_id", "assertion_status", "review_status", "event_date", "rule_id",
        "normalization_source_object_id", "normalization_source_sentence_id", "normalization_source_subject_id",
        "original_object_id", "original_subject_id",
    },
}


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_jsonl(path, rows):
    Path(path).write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build(source=SOURCE, destination=DESTINATION):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    source_manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    destination.mkdir(parents=True, exist_ok=True)
    source_relations = read_jsonl(source / "relations.jsonl")
    source_entities = read_jsonl(source / "entities.jsonl")
    connected_ids = {
        endpoint
        for relation in source_relations
        for endpoint in (relation["subject_id"], relation["object_id"])
    }
    source_isolates = {row["entity_id"] for row in source_entities} - connected_ids
    claim_endpoints = {
        endpoint
        for claim in read_jsonl(source / "claims.jsonl")
        for endpoint in (claim["subject_id"], claim["object_id"])
    }
    if source_isolates & claim_endpoints:
        raise ValueError("Cannot omit isolated entities referenced by retained claims")
    counts = {}
    source_fields = {}
    for kind, allowed in PUBLIC_FIELDS.items():
        rows = source_relations if kind == "relations" else read_jsonl(source / f"{kind}.jsonl")
        source_fields[kind] = set().union(*(row.keys() for row in rows))
        if kind == "entities":
            rows = [row for row in rows if row["entity_id"] in connected_ids]
        public_rows = [{key: value for key, value in row.items() if key in allowed} for row in rows]
        write_jsonl(destination / f"{kind}.jsonl", public_rows)
        counts[kind] = len(public_rows)

    entity_rows = read_jsonl(destination / "entities.jsonl")
    manifest = {
        "release": "v15-global-business-only-20261112",
        "source_export": source.name,
        "counts": {
            "articles": counts["articles"],
            "entities": len(entity_rows),
            "nodes": len(connected_ids),
            "isolated_entities": 0,
            "relations": counts["relations"],
            "claims": counts["claims"],
            "relation_types": source_manifest.get("counts", {}).get("relation_types"),
        },
        "source_counts": {
            "entity_rows": len(source_entities),
            "isolated_entities_omitted": len(source_isolates),
        },
        "source_export_manifest_sha256": sha256(source / "manifest.json"),
        "source_input_sha256": source_manifest.get("lineage", {}).get("input_sha256", {}),
        "file_sha256": {
            f"{kind}.jsonl": sha256(destination / f"{kind}.jsonl") for kind in PUBLIC_FIELDS
        },
        "public_projection": {
            "entity_scope": "only entities that are endpoints of at least one relation, matching the AuraDB graph projection",
            "omitted_fields": {
                f"{kind}.jsonl": sorted(source_fields[kind] - allowed)
                for kind, allowed in PUBLIC_FIELDS.items()
            },
            "evidence_status": "text and quote evidence omitted; use the group's access-controlled evidence bundle",
            "quality_status": "candidate graph; independent human-gold precision has not been measured",
        },
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out", type=Path, default=DESTINATION)
    args = parser.parse_args()
    result = build(args.source, args.out)
    print(json.dumps({"output": str(args.out.resolve()), "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
