"""Build a non-destructive, schema-strict graph projection of a normalized export."""
import argparse
import hashlib
import importlib
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
RELATION_TYPES = importlib.import_module("weconomy.schema").RELATION_TYPES
ENTITY_TYPES = {"PERSON", "ORG", "PLACE", "GOV"}
DEFAULT_SOURCE = ROOT / "data/normalized/international-business-v15-manual-20261112-global-business-only"
DEFAULT_OUTPUT = ROOT / "data/normalized/international-business-v15-manual-20261112-global-business-only-strict-candidate-20261122-v2"


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_jsonl(path, rows):
    Path(path).write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                          encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relation_reasons(row, entities):
    reasons = []
    subject = entities.get(row.get("subject_id"))
    object_ = entities.get(row.get("object_id"))
    if subject is None or object_ is None:
        reasons.append("missing_endpoint")
        return reasons
    subject_type, object_type = subject.get("entity_type"), object_.get("entity_type")
    if subject_type not in ENTITY_TYPES or object_type not in ENTITY_TYPES:
        reasons.append("endpoint_type_outside_schema")
    if row.get("predicate") in RELATION_TYPES:
        expected_subject, expected_object = RELATION_TYPES[row["predicate"]]
        if subject_type not in expected_subject or object_type not in expected_object:
            reasons.append("predicate_endpoint_type_violation")
    return reasons


def evidence_errors(rows, articles):
    missing_document = 0
    missing_text = 0
    bad_offset = 0
    for row in rows:
        article = articles.get(row.get("document_id"))
        if article is None:
            missing_document += 1
            continue
        evidence, text = row.get("evidence", ""), article.get("text", "")
        if not evidence or evidence not in text:
            missing_text += 1
        start, end = row.get("evidence_start"), row.get("evidence_end")
        if isinstance(start, int) and isinstance(end, int) and text[start:end] != evidence:
            bad_offset += 1
    return {"missing_documents": missing_document, "missing_evidence_text": missing_text,
            "bad_evidence_offsets": bad_offset}


def build(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_dir():
        raise FileNotFoundError(source)
    if output.exists():
        raise FileExistsError(f"Candidate path already exists; refusing to overwrite: {output}")
    if output == source or source in output.parents:
        raise ValueError("Candidate must be outside and separate from the source export")

    articles_all = read_jsonl(source / "articles.jsonl")
    entities_all = read_jsonl(source / "entities.jsonl")
    relations_all = read_jsonl(source / "relations.jsonl")
    claims_all = read_jsonl(source / "claims.jsonl")
    entities_by_id = {row["entity_id"]: row for row in entities_all}
    articles_by_id = {row["document_id"]: row for row in articles_all}
    if len(entities_by_id) != len(entities_all) or len(articles_by_id) != len(articles_all):
        raise ValueError("Source export has duplicate entity or article IDs; cannot project safely")

    rejected_relations = []
    valid_relations = []
    rejected_reasons = {}
    seen_triples = set()
    for row in relations_all:
        triple = (row["subject_id"], row["predicate"], row["object_id"])
        if triple in seen_triples:
            raise ValueError(f"Source export has duplicate graph triple: {triple}")
        seen_triples.add(triple)
        reasons = relation_reasons(row, entities_by_id)
        if reasons:
            rejected_relations.append({**row, "quarantine_reasons": reasons})
            rejected_reasons[triple] = reasons
        else:
            valid_relations.append(row)

    valid_triples = {(row["subject_id"], row["predicate"], row["object_id"])
                     for row in valid_relations}
    valid_claims, rejected_claims = [], []
    for row in claims_all:
        triple = (row["subject_id"], row["predicate"], row["object_id"])
        if triple in valid_triples:
            valid_claims.append(row)
        else:
            reasons = rejected_reasons.get(triple, ["claim_has_no_relation_row"])
            rejected_claims.append({**row, "quarantine_reasons": reasons})

    valid_node_ids = {node_id for row in valid_relations
                      for node_id in (row["subject_id"], row["object_id"])}
    valid_entities = [row for row in entities_all if row["entity_id"] in valid_node_ids]
    quarantined_entities = []
    for row in entities_all:
        if row["entity_id"] not in valid_node_ids:
            reason = ("entity_type_outside_schema" if row.get("entity_type") not in ENTITY_TYPES
                      else "no_remaining_valid_relation")
            quarantined_entities.append({**row, "quarantine_reason": reason})

    used_document_ids = {row["document_id"] for row in valid_relations + valid_claims}
    valid_articles = [row for row in articles_all if row["document_id"] in used_document_ids]
    valid_articles_by_id = {row["document_id"]: row for row in valid_articles}
    if len(valid_articles_by_id) != len(valid_articles):
        raise ValueError("Candidate article IDs are not unique")
    relation_evidence = evidence_errors(valid_relations, valid_articles_by_id)
    claim_evidence = evidence_errors(valid_claims, valid_articles_by_id)
    endpoint_missing_claims = sum(row["subject_id"] not in valid_node_ids or row["object_id"] not in valid_node_ids
                                  for row in valid_claims)
    if any(relation_evidence.values()) or any(claim_evidence.values()) or endpoint_missing_claims:
        raise ValueError("Filtered evidence/endpoint integrity check failed; candidate not written")

    counts = {
        "articles": len(valid_articles), "nodes": len(valid_node_ids),
        "relations": len(valid_relations), "claims": len(valid_claims),
        "relation_types": len({row["predicate"] for row in valid_relations}),
    }
    source_manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    targets = source_manifest.get("status", {}).get("targets") or {
        "nodes": 2000, "relations": 5000, "relation_types": 10}
    targets_met = all(counts.get(key, 0) >= value for key, value in targets.items() if value is not None)
    constraints = {key: {"subject": value[0], "object": value[1]}
                   for key, value in RELATION_TYPES.items()}
    candidate_manifest = {
        "format": "weconomy-strict-graph-candidate-v1",
        "storage_layer": "normalized",
        "candidate_only": True,
        "source_export": str(source),
        "counts": counts,
        "status": {"reason": "strict_graph_contract_projection", "targets": targets,
                   "targets_met": targets_met,
                   "remaining": {key: max(0, value - counts.get(key, 0))
                                 for key, value in targets.items() if value is not None}},
        "quality": {"precision": None,
                    "reason": "Requires independent human evaluation; this projection only enforces schema constraints."},
        "strict_projection": {
            "allowed_entity_types": sorted(ENTITY_TYPES), "predicate_endpoint_constraints": constraints,
            "source_relations": len(relations_all), "retained_relations": len(valid_relations),
            "quarantined_relations": len(rejected_relations), "quarantined_claims": len(rejected_claims),
            "quarantined_entities": len(quarantined_entities),
            "quarantine_reason_counts": dict(Counter(reason for row in rejected_relations
                                                        for reason in row["quarantine_reasons"])),
            "integrity": {"relation_evidence": relation_evidence, "claim_evidence": claim_evidence,
                          "claims_with_missing_candidate_endpoint": endpoint_missing_claims},
        },
        "lineage": {
            "source_manifest_sha256": digest(source / "manifest.json"),
            "input_sha256": {name: digest(source / f"{name}.jsonl")
                             for name in ("articles", "entities", "relations", "claims")},
            "builder_sha256": digest(Path(__file__)),
        },
        "audit": {"quarantined_entities": "audit/quarantined_entities.jsonl",
                  "quarantined_relations": "audit/quarantined_relations.jsonl",
                  "quarantined_claims": "audit/quarantined_claims.jsonl"},
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="strict-candidate-", dir=output.parent) as temp_dir:
        temp = Path(temp_dir)
        (temp / "audit").mkdir()
        write_jsonl(temp / "articles.jsonl", valid_articles)
        write_jsonl(temp / "entities.jsonl", valid_entities)
        write_jsonl(temp / "relations.jsonl", valid_relations)
        write_jsonl(temp / "claims.jsonl", valid_claims)
        write_jsonl(temp / "audit/quarantined_entities.jsonl", quarantined_entities)
        write_jsonl(temp / "audit/quarantined_relations.jsonl", rejected_relations)
        write_jsonl(temp / "audit/quarantined_claims.jsonl", rejected_claims)
        for name in ("articles", "entities", "relations", "claims"):
            candidate_manifest.setdefault("candidate_sha256", {})[name] = digest(temp / f"{name}.jsonl")
        (temp / "manifest.json").write_text(json.dumps(candidate_manifest, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
        temp.replace(output)

    return {"candidate": str(output), "counts": counts, "targets_met": targets_met,
            "remaining": candidate_manifest["status"]["remaining"],
            "quarantined": candidate_manifest["strict_projection"],
            "manifest": str(output / "manifest.json")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
