"""Prepare deterministic, full-population human review packets for the graph export."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT = ROOT / "data/normalized/international-business-v15-manual-20261112-global-business-only"
DEFAULT_OUTPUT = ROOT / "metrics/reviews/full-review-20261122"


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def context(text, start, end, radius=250):
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end > len(text):
        return text[:radius * 2]
    return text[max(0, start - radius):min(len(text), end + radius)]


def write_shards(rows, directory, prefix, shard_size):
    paths = []
    for start in range(0, len(rows), shard_size):
        shard = rows[start:start + shard_size]
        first, last = start + 1, start + len(shard)
        path = directory / f"{prefix}-{first:04d}-{last:04d}.jsonl"
        write_jsonl(path, shard)
        paths.append({"path": str(path.resolve()), "count": len(shard), "sha256": digest(path)})
    return paths


def prepare(export, output, shard_size):
    export, output = Path(export).resolve(), Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty review directory: {output}")
    articles = {row["document_id"]: row for row in read_jsonl(export / "articles.jsonl")}
    entities = read_jsonl(export / "entities.jsonl")
    entities_by_id = {row["entity_id"]: row for row in entities}
    relations = read_jsonl(export / "relations.jsonl")
    claims = read_jsonl(export / "claims.jsonl")

    edge_tasks = []
    connected = set()
    claims_by_entity = defaultdict(list)
    for index, row in enumerate(relations, 1):
        article = articles[row["document_id"]]
        subject = entities_by_id[row["subject_id"]]
        object_ = entities_by_id[row["object_id"]]
        connected.update((row["subject_id"], row["object_id"]))
        edge_tasks.append({
            "task_id": f"edge-{index:05d}", "claim_id": row["claim_id"],
            "subject": {"entity_id": subject["entity_id"], "name": subject["name"],
                        "type": subject["entity_type"]},
            "predicate": row["predicate"],
            "object": {"entity_id": object_["entity_id"], "name": object_["name"],
                       "type": object_["entity_type"]},
            "assertion_status": row.get("assertion_status", ""),
            "evidence": row.get("evidence", ""),
            "context": context(article.get("text", ""), row.get("evidence_start"), row.get("evidence_end")),
            "url": article.get("canonical_url", ""), "title": article.get("title", ""),
            "source": urlsplit(article.get("canonical_url", "")).hostname or "unknown",
            "language": article.get("language", "unknown"), "document_id": row["document_id"],
            "verdict": "", "reviewer": "", "complete": False, "review_note": "",
        })
    for row in claims:
        for entity_id in {row.get("subject_id"), row.get("object_id")}:
            if entity_id in entities_by_id:
                claims_by_entity[entity_id].append(row)

    node_tasks = []
    for index, entity in enumerate(entities, 1):
        examples = []
        seen_documents = set()
        for claim in claims_by_entity.get(entity["entity_id"], []):
            if claim["document_id"] in seen_documents:
                continue
            article = articles.get(claim["document_id"], {})
            examples.append({
                "predicate": claim.get("predicate", ""),
                "role": "subject" if claim.get("subject_id") == entity["entity_id"] else "object",
                "other_entity": entities_by_id.get(
                    claim.get("object_id") if claim.get("subject_id") == entity["entity_id"]
                    else claim.get("subject_id"), {}).get("name", ""),
                "evidence": claim.get("evidence", ""),
                "context": context(article.get("text", ""), claim.get("evidence_start"), claim.get("evidence_end")),
                "url": article.get("canonical_url", ""),
                "language": article.get("language", "unknown"),
            })
            seen_documents.add(claim["document_id"])
            if len(examples) == 5:
                break
        node_tasks.append({
            "task_id": f"node-{index:05d}", "entity_id": entity["entity_id"],
            "candidate_name": entity.get("name", ""), "candidate_type": entity.get("entity_type", ""),
            "connected_in_graph": entity["entity_id"] in connected,
            "evidence_examples": examples, "evidence_count": len(claims_by_entity.get(entity["entity_id"], [])),
            "verdict": "", "reviewer": "", "complete": False, "review_note": "",
        })

    output.mkdir(parents=True, exist_ok=True)
    edge_shards = write_shards(edge_tasks, output / "edges", "edges", shard_size)
    node_shards = write_shards(node_tasks, output / "nodes", "nodes", shard_size)
    source_files = ("articles.jsonl", "entities.jsonl", "relations.jsonl", "claims.jsonl", "manifest.json")
    manifest = {
        "export": str(export), "created": "2026-11-22", "coverage": "full_population_deterministic_order",
        "counts": {"relations": len(edge_tasks), "entity_rows": len(node_tasks),
                   "connected_nodes": len(connected), "claims": len(claims)},
        "input_sha256": {name: digest(export / name) for name in source_files},
        "shard_size": shard_size, "edges": edge_shards, "nodes": node_shards,
        "label_schema": ["correct", "incorrect", "uncertain"],
        "note": "Review every row. AI labels are not human gold. Do not overwrite or edit the source export.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, default=DEFAULT_EXPORT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--shard-size", type=int, default=100)
    args = parser.parse_args()
    if args.shard_size < 1:
        parser.error("--shard-size must be positive")
    result = prepare(args.export, args.out_dir, args.shard_size)
    print(json.dumps({"output": str(args.out_dir.resolve()), "counts": result["counts"],
                      "edge_shards": len(result["edges"]), "node_shards": len(result["nodes"]),
                      "source_hashes": result["input_sha256"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
