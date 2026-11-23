"""Score completed human labels against the pinned 300-item random gold sample."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def wilson(correct, n, z=1.959963984540054):
    if not n:
        return None
    p = correct / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [max(0.0, center - margin), min(1.0, center + margin)]


def score(manifest_path, labels_dir, kind):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    expected_rows = [row for shard in manifest[kind] for row in read_jsonl(shard["path"])]
    expected = {row["task_id"] for row in expected_rows}
    prefix = "edge-" if kind == "edges" else "node-"
    observed, duplicates = {}, []
    for path in sorted(Path(labels_dir).rglob("*.jsonl")):
        for row in read_jsonl(path):
            task_id = row.get("task_id")
            if isinstance(task_id, str) and task_id.startswith(prefix):
                if task_id in observed:
                    duplicates.append(task_id)
                observed[task_id] = row
    unknown = sorted(set(observed) - expected)
    incomplete = sorted(task_id for task_id, row in observed.items() if task_id in expected and
                        (row.get("verdict") not in {"correct", "incorrect", "uncertain"} or
                         not row.get("reviewer") or row.get("complete") is not True))
    valid = {task_id: row for task_id, row in observed.items()
             if task_id in expected and task_id not in incomplete}
    verdicts = Counter(row["verdict"] for row in valid.values())
    n = len(valid)
    is_complete = n == len(expected) and not duplicates and not unknown
    conservative_correct = verdicts["correct"]
    result = {
        "kind": kind,
        "reviewer_kind": "human",
        "export": manifest["export"],
        "selection": manifest["selection"],
        "seed": manifest["seed"],
        "source_population_size": manifest["populations"]["edges" if kind == "edges" else "connected_nodes"],
        "sample_size": len(expected),
        "valid_labels": n,
        "sample_coverage": n / len(expected) if expected else 0.0,
        "full_sample_complete": is_complete,
        "verdicts": dict(verdicts),
        "unknown_task_ids": unknown,
        "duplicate_task_ids": sorted(set(duplicates)),
        "missing_task_count": len(expected - set(observed)),
        "incomplete_task_count": len(incomplete),
        "estimated_precision": conservative_correct / n if n else None,
        "wilson_95_interval": wilson(conservative_correct, n),
        "target_lower_bound_at_least_90_percent": bool(is_complete and wilson(conservative_correct, n)[0] >= 0.90),
        "interpretation": "Sample estimate only; uncertain labels count as incorrect. Do not claim a census precision score.",
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--labels-dir", type=Path, required=True)
    parser.add_argument("--kind", choices=("edges", "nodes"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = score(args.manifest, args.labels_dir, args.kind)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("kind", "sample_size", "valid_labels", "sample_coverage",
                                               "verdicts", "estimated_precision", "wilson_95_interval",
                                               "target_lower_bound_at_least_90_percent")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
