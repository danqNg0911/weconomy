"""Verify coverage and summarize labels for full-population review packets."""
import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def score(manifest_path, labels_dir, kind, reviewer_kind):
    manifest_path, labels_dir = Path(manifest_path), Path(labels_dir)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_rows = []
    for shard in manifest[kind]:
        expected_rows.extend(read_jsonl(shard["path"]))
    expected = {row["task_id"]: row for row in expected_rows}
    observed = {}
    duplicates = []
    prefix = "edge-" if kind == "edges" else "node-"
    for path in sorted(labels_dir.rglob("*.jsonl")):
        for row in read_jsonl(path):
            task_id = row.get("task_id")
            if not isinstance(task_id, str) or not task_id.startswith(prefix):
                continue
            if task_id in observed:
                duplicates.append(task_id)
            observed[task_id] = row
    unknown = sorted(set(observed) - set(expected))
    incomplete = sorted(task_id for task_id, row in observed.items()
                        if task_id in expected and (row.get("verdict") not in
                        {"correct", "incorrect", "uncertain"} or not row.get("reviewer") or
                        row.get("complete") is not True))
    missing = sorted(set(expected) - set(observed))
    valid = {task_id: row for task_id, row in observed.items()
             if task_id in expected and task_id not in incomplete}
    verdicts = Counter(row["verdict"] for row in valid.values())
    coverage = len(valid) / len(expected) if expected else 0.0
    full = len(valid) == len(expected) and not duplicates and not unknown
    correct_share = verdicts["correct"] / len(valid) if valid else None
    result = {
        "kind": kind, "reviewer_kind": reviewer_kind, "export": manifest["export"],
        "input_sha256": manifest["input_sha256"],
        "population": len(expected), "valid_labels": len(valid), "coverage": coverage,
        "full_population_complete": full, "verdicts": dict(verdicts),
        "missing_task_count": len(missing), "incomplete_task_count": len(incomplete),
        "duplicate_task_ids": sorted(set(duplicates)), "unknown_task_ids": unknown,
        "precision": correct_share if full and reviewer_kind == "human" else None,
        "ai_screen_correct_share": correct_share if reviewer_kind == "ai" else None,
        "interpretation": (
            "Exact score for the pinned population after full human review and adjudication."
            if full and reviewer_kind == "human" else
            "Full AI-screen verdict share; not verified precision."
            if full and reviewer_kind == "ai" else
            "Partial review only; do not report population precision."
        ),
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--labels-dir", type=Path, required=True)
    parser.add_argument("--kind", choices=("edges", "nodes"), required=True)
    parser.add_argument("--reviewer-kind", choices=("ai", "human"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = score(args.manifest, args.labels_dir, args.kind, args.reviewer_kind)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in
                      ("kind", "reviewer_kind", "population", "valid_labels", "coverage",
                       "full_population_complete", "verdicts", "precision", "ai_screen_correct_share")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
