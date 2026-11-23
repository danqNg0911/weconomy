"""Prepare blind review samples and score the current normalized graph export."""
import argparse
import hashlib
import importlib
import json
import random
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
RELATION_TYPES = importlib.import_module("weconomy.schema").RELATION_TYPES

DEFAULT_EXPORT = ROOT / "data/normalized/international-business-v15-manual-20261112-global-business-only"
SAMPLE_DIR = ROOT / "metrics/samples"
RESULT_DIR = ROOT / "metrics/results"
SEED = 20261122
ENTITY_TYPES = {"PERSON", "ORG", "PLACE", "GOV"}


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit_export(export):
    export = Path(export)
    articles = read_jsonl(export / "articles.jsonl")
    entities = read_jsonl(export / "entities.jsonl")
    relations = read_jsonl(export / "relations.jsonl")
    claims = read_jsonl(export / "claims.jsonl")
    entity_by_id = {row["entity_id"]: row for row in entities}
    article_by_id = {row["document_id"]: row for row in articles}
    triples = [(r["subject_id"], r["predicate"], r["object_id"]) for r in relations]
    connected = {entity_id for r in relations for entity_id in (r["subject_id"], r["object_id"])}
    claim_triples = {(r["subject_id"], r["predicate"], r["object_id"]) for r in claims}
    missing_endpoints = sum(r["subject_id"] not in entity_by_id or r["object_id"] not in entity_by_id
                            for r in relations)
    bad_evidence = sum(r.get("document_id") not in article_by_id or not r.get("evidence") or
                       r["evidence"] not in article_by_id[r["document_id"]].get("text", "")
                       for r in relations)
    bad_offsets = sum(isinstance(r.get("evidence_start"), int) and isinstance(r.get("evidence_end"), int)
                      and article_by_id.get(r.get("document_id"), {}).get("text", "")
                      [r["evidence_start"]:r["evidence_end"]] != r.get("evidence") for r in relations)
    missing_claim_endpoints = sum(r.get("subject_id") not in entity_by_id or
                                  r.get("object_id") not in entity_by_id for r in claims)
    bad_claim_evidence = sum(r.get("document_id") not in article_by_id or not r.get("evidence") or
                             r["evidence"] not in article_by_id[r["document_id"]].get("text", "")
                             for r in claims)
    bad_claim_offsets = sum(isinstance(r.get("evidence_start"), int) and
                            isinstance(r.get("evidence_end"), int) and
                            article_by_id.get(r.get("document_id"), {}).get("text", "")
                            [r["evidence_start"]:r["evidence_end"]] != r.get("evidence") for r in claims)
    forbidden_names = {"vinpearl": 0, "vietnam airlines": 0}
    for entity in entities:
        name = entity.get("name", "").casefold()
        for forbidden in forbidden_names:
            forbidden_names[forbidden] += forbidden in name
    outside_schema_rows = [row for row in entities if row.get("entity_type") not in ENTITY_TYPES]
    connected_outside_schema = [entity_by_id[entity_id] for entity_id in connected
                                if entity_id in entity_by_id and
                                entity_by_id[entity_id].get("entity_type") not in ENTITY_TYPES]
    invalid_endpoint_edges = []
    endpoint_type_violations = []
    invalid_endpoint_triples = set()
    endpoint_violation_triples = set()
    all_triples = set()
    predicate_counts = Counter()
    status_counts = Counter()
    assertion_counts = Counter()
    language_counts = Counter()
    source_counts = Counter()
    predicate_type_violations = Counter()
    for row in relations:
        triple = (row["subject_id"], row["predicate"], row["object_id"])
        all_triples.add(triple)
        subject_type = entity_by_id.get(row["subject_id"], {}).get("entity_type", "MISSING")
        object_type = entity_by_id.get(row["object_id"], {}).get("entity_type", "MISSING")
        predicate_counts[row["predicate"]] += 1
        status_counts[row.get("review_status") or "missing"] += 1
        assertion_counts[row.get("assertion_status") or "missing"] += 1
        article = article_by_id.get(row.get("document_id"), {})
        language_counts[article.get("language", "unknown")] += 1
        source_counts[urlsplit(article.get("canonical_url", "")).hostname or "unknown"] += 1
        if subject_type not in ENTITY_TYPES or object_type not in ENTITY_TYPES:
            invalid_endpoint_edges.append(row)
            invalid_endpoint_triples.add((row["subject_id"], row["predicate"], row["object_id"]))
        if row["predicate"] in RELATION_TYPES:
            expected_subject, expected_object = RELATION_TYPES[row["predicate"]]
            if subject_type not in expected_subject or object_type not in expected_object:
                endpoint_type_violations.append(row)
                predicate_type_violations[row["predicate"]] += 1
                endpoint_violation_triples.add((row["subject_id"], row["predicate"], row["object_id"]))
    invalid_triples = invalid_endpoint_triples | endpoint_violation_triples
    retained_relations = [row for row in relations
                          if (row["subject_id"], row["predicate"], row["object_id"]) not in invalid_triples]
    retained_nodes = {node_id for row in retained_relations for node_id in
                      (row["subject_id"], row["object_id"])}
    manifest = json.loads((export / "manifest.json").read_text(encoding="utf-8"))
    checks = {
        "duplicate_article_ids": len(articles) - len(article_by_id),
        "duplicate_entity_ids": len(entities) - len(entity_by_id),
        "duplicate_relation_claim_ids": len(relations) - len({r.get("claim_id") for r in relations}),
        "duplicate_claim_ids": len(claims) - len({r.get("claim_id") for r in claims}),
        "duplicate_triples": len(triples) - len(set(triples)),
        "missing_endpoints": missing_endpoints,
        "missing_claim_endpoints": missing_claim_endpoints,
        "bad_or_missing_evidence": bad_evidence,
        "bad_evidence_offsets": bad_offsets,
        "bad_or_missing_claim_evidence": bad_claim_evidence,
        "bad_claim_evidence_offsets": bad_claim_offsets,
        "self_edges": sum(a == b for a, _, b in triples),
        "unevidenced_triples": len(set(triples) - claim_triples),
        "unconnected_entities": len(set(entity_by_id) - connected),
        "vinpearl_entity_matches": forbidden_names["vinpearl"],
        "vietnam_airlines_entity_matches": forbidden_names["vietnam airlines"],
        "manifest_counts_match": (
            manifest.get("counts", {}).get("articles") == len(articles)
            and manifest.get("counts", {}).get("nodes") == len(connected)
            and manifest.get("counts", {}).get("relations") == len(relations)
            and manifest.get("counts", {}).get("claims") == len(claims)
            and manifest.get("counts", {}).get("relation_types") == len({r["predicate"] for r in relations})
        ),
    }
    failed = [key for key, value in checks.items() if key != "unconnected_entities" and
              (value is False or (type(value) is int and value != 0))]
    return {
        "export": str(export.resolve()),
        "counts": {"articles": len(articles), "entity_rows": len(entities), "connected_nodes": len(connected),
                   "relations": len(relations), "claims": len(claims),
                   "relation_types": len({r["predicate"] for r in relations})},
        "structural_checks": checks,
        "structural_checks_passed": not failed,
        "failed_checks": failed,
        "precision": None,
        "precision_note": "Requires completed independent human labels; structural validation is not precision.",
        "input_sha256": {name: sha256(export / f"{name}.jsonl")
                         for name in ("articles", "entities", "relations", "claims")},
        "full_profile": {
            "review_status_counts": dict(status_counts),
            "assertion_status_counts": dict(assertion_counts),
            "relation_counts_by_predicate": dict(sorted(predicate_counts.items())),
            "relation_counts_by_article_language": dict(language_counts),
            "relation_counts_by_source_host": dict(source_counts),
            "entity_rows_by_type": dict(Counter(row.get("entity_type", "missing") for row in entities)),
            "connected_nodes_by_type": dict(Counter(row.get("entity_type", "missing")
                                                     for row in connected_outside_schema +
                                                     [entity_by_id[i] for i in connected
                                                      if i in entity_by_id and
                                                      entity_by_id[i].get("entity_type") in ENTITY_TYPES])),
            "entity_rows_outside_schema": len(outside_schema_rows),
            "connected_nodes_outside_schema": len(connected_outside_schema),
            "edges_with_endpoint_outside_schema": len(invalid_endpoint_edges),
            "mapped_relation_endpoint_violations": len(endpoint_type_violations),
            "unique_edges_with_any_graph_contract_violation": len(invalid_endpoint_triples |
                                                                  endpoint_violation_triples),
            "contract_filter_projection": {
                "retained_edges": len(retained_relations),
                "retained_connected_nodes": len(retained_nodes),
                "retained_relation_types": len({row["predicate"] for row in retained_relations}),
                "removed_edges": len(relations) - len(retained_relations),
                "meets_2000_node_5000_edge_10_type_targets": (
                    len(retained_nodes) >= 2000 and len(retained_relations) >= 5000
                    and len({row["predicate"] for row in retained_relations}) >= 10
                ),
                "note": "Projection only; no source export or graph data is modified.",
            },
            "violations_by_predicate": dict(predicate_type_violations),
            "graph_contract_passed": not connected_outside_schema and not endpoint_type_violations,
            "note": "Review status is provenance, not independent gold accuracy; schema violations are exhaustive counts.",
        },
    }


def context_for(text, start, end, radius=350):
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end > len(text):
        return text[:radius * 2]
    return text[max(0, start - radius):min(len(text), end + radius)]


def prepare(export, out_dir, edge_n=400, node_n=300, seed=SEED):
    export, out_dir = Path(export), Path(out_dir)
    articles = {r["document_id"]: r for r in read_jsonl(export / "articles.jsonl")}
    entities = {r["entity_id"]: r for r in read_jsonl(export / "entities.jsonl")}
    relations = read_jsonl(export / "relations.jsonl")
    rng = random.Random(seed)

    selected_edges = rng.sample(relations, min(edge_n, len(relations)))
    edge_tasks = []
    for index, row in enumerate(selected_edges, 1):
        article = articles[row["document_id"]]
        subject, object_ = entities[row["subject_id"]], entities[row["object_id"]]
        edge_tasks.append({
            "task_id": f"edge-{index:04d}", "relation_id": row.get("relation_id", row["claim_id"]),
            "subject": {"name": subject["name"], "type": subject["entity_type"]},
            "predicate": row["predicate"],
            "object": {"name": object_["name"], "type": object_["entity_type"]},
            "assertion_status": row.get("assertion_status", ""),
            "evidence": row.get("evidence", ""),
            "context": context_for(article.get("text", ""), row.get("evidence_start"), row.get("evidence_end")),
            "url": article.get("canonical_url", ""), "title": article.get("title", ""),
            "source": urlsplit(article.get("canonical_url", "")).hostname or "unknown",
            "language": article.get("language", "unknown"), "document_id": row["document_id"],
            "verdict": "", "reviewer": "", "complete": False, "review_note": "",
        })

    adjacency = defaultdict(list)
    for row in relations:
        adjacency[row["subject_id"]].append((row, row["object_id"], "subject"))
        adjacency[row["object_id"]].append((row, row["subject_id"], "object"))
    connected_ids = list(adjacency)
    selected_nodes = rng.sample(connected_ids, min(node_n, len(connected_ids)))
    node_tasks = []
    for index, entity_id in enumerate(selected_nodes, 1):
        entity = entities[entity_id]
        row, other_id, role = rng.choice(adjacency[entity_id])
        article = articles[row["document_id"]]
        node_tasks.append({
            "task_id": f"node-{index:04d}", "entity_id": entity_id,
            "candidate_name": entity["name"], "candidate_type": entity["entity_type"],
            "example_relation": {"role": role, "predicate": row["predicate"],
                                 "other_entity": entities[other_id]["name"]},
            "evidence": row.get("evidence", ""),
            "context": context_for(article.get("text", ""), row.get("evidence_start"), row.get("evidence_end")),
            "url": article.get("canonical_url", ""), "title": article.get("title", ""),
            "source": urlsplit(article.get("canonical_url", "")).hostname or "unknown",
            "language": article.get("language", "unknown"), "document_id": row["document_id"],
            "verdict": "", "reviewer": "", "complete": False, "review_note": "",
        })

    edge_path, node_path = out_dir / "edges-review.jsonl", out_dir / "nodes-review.jsonl"
    write_jsonl(edge_path, edge_tasks)
    write_jsonl(node_path, node_tasks)
    edge_double = rng.sample(edge_tasks, max(1, round(len(edge_tasks) * 0.20))) if edge_tasks else []
    node_double = rng.sample(node_tasks, max(1, round(len(node_tasks) * 0.20))) if node_tasks else []
    def independent_copy(task):
        return {**task, "verdict": "", "reviewer": "", "complete": False, "review_note": ""}
    edge_double_path, node_double_path = out_dir / "edges-double-review.jsonl", out_dir / "nodes-double-review.jsonl"
    write_jsonl(edge_double_path, [independent_copy(row) for row in edge_double])
    write_jsonl(node_double_path, [independent_copy(row) for row in node_double])
    metadata = {
        "created": date.today().isoformat(), "export": str(export.resolve()), "seed": seed,
        "edge_population": len(relations), "node_population": len(connected_ids),
        "edge_sample_size": len(edge_tasks), "node_sample_size": len(node_tasks),
        "sampling": "simple random sample without replacement; fixed seed",
        "input_sha256": {name: sha256(export / f"{name}.jsonl")
                         for name in ("articles", "entities", "relations", "claims")},
        "samples": {"edges": {"path": str(edge_path), "sha256": sha256(edge_path)},
                    "nodes": {"path": str(node_path), "sha256": sha256(node_path)},
                    "edges_double_review": {"path": str(edge_double_path), "sha256": sha256(edge_double_path),
                                            "size": len(edge_double)},
                    "nodes_double_review": {"path": str(node_double_path), "sha256": sha256(node_double_path),
                                            "size": len(node_double)}},
        "note": "Do not train/tune on these review tasks. Keep reviewer copies separate; adjudicate disagreements.",
    }
    write_json(out_dir / "sample-manifest.json", metadata)
    return metadata


def wilson(tp, total):
    if not total:
        return None
    p, z = tp / total, 1.96
    denominator = 1 + z * z / total
    center = p + z * z / (2 * total)
    margin = z * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5)
    return [max(0.0, (center - margin) / denominator), min(1.0, (center + margin) / denominator)]


def score_file(path, dimensions):
    tasks = read_jsonl(path)
    allowed = {"correct", "incorrect", "uncertain"}
    if len({task.get("task_id") for task in tasks}) != len(tasks):
        raise ValueError("Review file contains duplicate task_id values")
    for task in tasks:
        if not task.get("complete") or not task.get("reviewer"):
            raise ValueError(f"Incomplete review or missing reviewer: {task['task_id']}")
        if task.get("verdict") not in allowed:
            raise ValueError(f"Invalid verdict in {task['task_id']}; use correct/incorrect/uncertain")
    tp = sum(t["verdict"] == "correct" for t in tasks)
    uncertain = sum(t["verdict"] == "uncertain" for t in tasks)
    # Uncertain cases count as incorrect until adjudicated, avoiding optimistic precision.
    groups = {}
    for dimension in dimensions:
        buckets = defaultdict(list)
        for task in tasks:
            buckets[str(task.get(dimension, "unknown"))].append(task)
        groups[dimension] = {
            key: {"n": len(rows), "correct": sum(r["verdict"] == "correct" for r in rows),
                  "uncertain": sum(r["verdict"] == "uncertain" for r in rows),
                  "precision": sum(r["verdict"] == "correct" for r in rows) / len(rows),
                  "wilson_95": wilson(sum(r["verdict"] == "correct" for r in rows), len(rows)),
                  "interpretation": "descriptive; subgroup sample may be too small"}
            for key, rows in sorted(buckets.items())
        }
    result = {"review_file": str(Path(path).resolve()), "n": len(tasks), "tp": tp,
              "fp_including_uncertain": len(tasks) - tp, "uncertain": uncertain,
              "precision_conservative": tp / len(tasks) if tasks else None,
              "wilson_95": wilson(tp, len(tasks)), "minimum_precision": 0.90,
              "passes_90_percent": bool(tasks) and wilson(tp, len(tasks))[0] >= 0.90,
              "group_metrics": groups,
              "note": "Uncertain is counted as incorrect; Wilson interval assumes independent sampled items."}
    return result


def agreement(first_path, second_path):
    first = {r["task_id"]: r for r in read_jsonl(first_path)}
    second = {r["task_id"]: r for r in read_jsonl(second_path)}
    if not second or not second.keys() <= first.keys():
        raise ValueError("Double-review task IDs must be a non-empty subset of the primary review file")
    first = {key: first[key] for key in second}
    if any(not r.get("complete") or not r.get("reviewer") or r.get("verdict") not in
           {"correct", "incorrect", "uncertain"} for r in (*first.values(), *second.values())):
        raise ValueError("Both reviewers must complete every task with a valid verdict")
    if any(first[key]["reviewer"] == second[key]["reviewer"] for key in first):
        raise ValueError("Double review must use two different reviewers")
    labels = ("correct", "incorrect", "uncertain")
    observed = sum(first[key]["verdict"] == second[key]["verdict"] for key in first) / len(first)
    expected = sum(
        sum(row["verdict"] == label for row in first.values()) / len(first) *
        sum(row["verdict"] == label for row in second.values()) / len(second)
        for label in labels
    )
    kappa = (observed - expected) / (1 - expected) if expected < 1 else None
    return {"n_double_reviewed": len(first), "raw_agreement": observed, "cohen_kappa": kappa,
            "first_review": str(Path(first_path).resolve()),
            "second_review": str(Path(second_path).resolve()),
            "note": "Adjudicate disagreements before scoring the primary review sample."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit", help="Run structural checks and save a baseline report")
    audit.add_argument("--export", type=Path, default=DEFAULT_EXPORT)
    audit.add_argument("--out", type=Path, default=RESULT_DIR / "v15-global-business-only-full-audit.json")
    prep = commands.add_parser("prepare", help="Create blind random review samples for graph edges and nodes")
    prep.add_argument("--export", type=Path, default=DEFAULT_EXPORT)
    prep.add_argument("--out-dir", type=Path, default=SAMPLE_DIR / "v15-global-business-only")
    prep.add_argument("--edges", type=int, default=400)
    prep.add_argument("--nodes", type=int, default=300)
    prep.add_argument("--seed", type=int, default=SEED)
    score = commands.add_parser("score", help="Score a completed reviewer JSONL file")
    score.add_argument("review_file", type=Path)
    score.add_argument("--kind", choices=("edges", "nodes"), required=True)
    score.add_argument("--out", type=Path, required=True)
    compare = commands.add_parser("agreement", help="Measure agreement on the double-reviewed subset")
    compare.add_argument("first_review", type=Path)
    compare.add_argument("second_review", type=Path)
    compare.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "audit":
        result = audit_export(args.export)
        write_json(args.out, result)
        lines = ["# Graph structural audit", "", f"Export: `{result['export']}`", "",
                 "| Measure | Result |", "|---|---:|"]
        lines.extend(f"| {key} | {value:,} |" for key, value in result["counts"].items())
        lines += ["", f"Structural checks passed: **{result['structural_checks_passed']}**", "",
                  "| Check | Result |", "|---|---:|"]
        lines.extend(f"| {key} | {value:,} |" if type(value) is int else f"| {key} | {value} |"
                     for key, value in result["structural_checks"].items())
        profile = result["full_profile"]
        lines += ["", f"Graph schema checks passed: **{profile['graph_contract_passed']}**", "",
                  "## Full-export profile", "", "| Measure | Count |", "|---|---:|"]
        for key, label in (("entity_rows_outside_schema", "Entity rows outside schema types"),
                           ("connected_nodes_outside_schema", "Connected nodes outside schema types"),
                           ("edges_with_endpoint_outside_schema", "Edges with an out-of-schema endpoint"),
                           ("mapped_relation_endpoint_violations", "Mapped predicate endpoint type violations"),
                           ("unique_edges_with_any_graph_contract_violation", "Unique edges to quarantine/review")):
            lines.append(f"| {label} | {profile[key]:,} |")
        projection = profile["contract_filter_projection"]
        lines.append(f"| Projected strict graph | {projection['retained_connected_nodes']:,} nodes, "
                     f"{projection['retained_edges']:,} edges, {projection['retained_relation_types']:,} types |")
        lines += ["", "### Relation status", "", "| Status | Edges |", "|---|---:|"]
        lines.extend(f"| {key} | {value:,} |" for key, value in sorted(profile["review_status_counts"].items()))
        lines += ["", "### Predicate counts", "", "| Predicate | Edges |", "|---|---:|"]
        lines.extend(f"| {key} | {value:,} |" for key, value in
                     sorted(profile["relation_counts_by_predicate"].items(), key=lambda item: -item[1]))
        lines += ["", "**Precision: unmeasured.** Structural checks do not establish extraction accuracy.",
                  "Review status is not an independent precision measurement.",
                  "Entity rows without graph edges are reported separately and excluded from connected-node count.", ""]
        Path(args.out).with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
        print(json.dumps({"output": str(args.out), "counts": result["counts"],
                          "structural_checks_passed": result["structural_checks_passed"],
                          "precision": None}, ensure_ascii=False))
    elif args.command == "prepare":
        result = prepare(args.export, args.out_dir, args.edges, args.nodes, args.seed)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "score":
        dimensions = ("predicate", "language", "source") if args.kind == "edges" else ("candidate_type", "language", "source")
        result = score_file(args.review_file, dimensions)
        write_json(args.out, result)
        print(json.dumps({"output": str(args.out), "n": result["n"],
                          "precision": result["precision_conservative"],
                          "wilson_95": result["wilson_95"],
                          "passes_90_percent": result["passes_90_percent"]}, ensure_ascii=False))
    else:
        result = agreement(args.first_review, args.second_review)
        write_json(args.out, result)
        print(json.dumps({"output": str(args.out), "n_double_reviewed": result["n_double_reviewed"],
                          "raw_agreement": result["raw_agreement"], "cohen_kappa": result["cohen_kappa"]},
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
