"""Prepare a blind, reproducible human-gold sample from the pinned full review population."""
import argparse
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW = ROOT / "metrics/reviews/full-review-20261122"
DEFAULT_OUTPUT = ROOT / "metrics/reviews/human-gold-20261123"
SEED = 20261123
SAMPLE_SIZE = 150


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def population(review_dir, manifest, kind):
    rows = []
    for shard in manifest[kind]:
        rows.extend(read_jsonl(shard["path"]))
    if len({row["task_id"] for row in rows}) != len(rows):
        raise ValueError(f"Duplicate task IDs in {kind} population")
    return rows


def blank_labels(rows):
    return [{**row, "verdict": "", "reviewer": "", "complete": False, "review_note": ""}
            for row in rows]


def prepare(review_dir, output, seed=SEED, size=SAMPLE_SIZE):
    review_dir, output = Path(review_dir).resolve(), Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty sample directory: {output}")
    source_manifest_path = review_dir / "manifest.json"
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    edge_population = population(review_dir, source_manifest, "edges")
    node_population_all = population(review_dir, source_manifest, "nodes")
    node_population = [row for row in node_population_all if row.get("connected_in_graph") is True]
    if len(edge_population) < size or len(node_population) < size:
        raise ValueError("Population is smaller than requested sample")

    rng = random.Random(seed)
    edges = blank_labels(rng.sample(edge_population, size))
    nodes = blank_labels(rng.sample(node_population, size))
    output.mkdir(parents=True, exist_ok=True)
    edge_path, node_path = output / "edges-review.jsonl", output / "nodes-review.jsonl"
    write_jsonl(edge_path, edges)
    write_jsonl(node_path, nodes)
    manifest = {
        "purpose": "locked_human_gold_validation",
        "export": source_manifest["export"],
        "selection": "simple_random_without_replacement_per_population",
        "seed": seed,
        "sample_size_each": size,
        "populations": {"edges": len(edge_population), "connected_nodes": len(node_population),
                        "entity_rows_including_disconnected": len(node_population_all)},
        "selected_task_ids": {"edges": [row["task_id"] for row in edges],
                               "nodes": [row["task_id"] for row in nodes]},
        "source_review_manifest": str(source_manifest_path),
        "source_input_sha256": source_manifest["input_sha256"],
        "sample_sha256": {"edges-review.jsonl": digest(edge_path),
                          "nodes-review.jsonl": digest(node_path)},
        "files": {"edges": str(edge_path.resolve()), "nodes": str(node_path.resolve())},
        "edges": [{"path": str(edge_path.resolve()), "count": len(edges), "sha256": digest(edge_path)}],
        "nodes": [{"path": str(node_path.resolve()), "count": len(nodes), "sha256": digest(node_path)}],
        # Compatible shard shape lets the existing coverage scorer verify exact sample IDs.
        "edges": [{"path": str(edge_path.resolve()), "count": len(edges), "sha256": digest(edge_path)}],
        "nodes": [{"path": str(node_path.resolve()), "count": len(nodes), "sha256": digest(node_path)}],
        "label_schema": ["correct", "incorrect", "uncertain"],
        "label_policy": "Mark uncertain as incorrect in the conservative score until adjudicated.",
        "blinding": "No AI verdict, extraction rule, model or review status is included.",
        "holdout_policy": "Do not use these human labels to tune thresholds and then report them as a locked test.",
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-dir", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--size", type=int, default=SAMPLE_SIZE)
    args = parser.parse_args()
    result = prepare(args.review_dir, args.out_dir, args.seed, args.size)
    print(json.dumps({"output": str(args.out_dir.resolve()), "sample_size_each": result["sample_size_each"],
                      "populations": result["populations"], "seed": result["seed"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
