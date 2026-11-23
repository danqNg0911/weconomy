"""Build a full-population review summary and non-correct case ledger."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from score_full_review import read_jsonl, score


def summarize(manifest_path, labels_dir, kind, reviewer_kind):
    manifest_path, labels_dir = Path(manifest_path), Path(labels_dir)
    coverage = score(manifest_path, labels_dir, kind, reviewer_kind)
    prefix = "edge-" if kind == "edges" else "node-"
    rows = [row for path in sorted(labels_dir.rglob("*.jsonl")) for row in read_jsonl(path)
            if isinstance(row.get("task_id"), str) and row["task_id"].startswith(prefix)]
    dimensions = ("predicate", "source", "language") if kind == "edges" else ("candidate_type",)
    grouped = {}
    for dimension in dimensions:
        buckets = defaultdict(Counter)
        for row in rows:
            buckets[str(row.get(dimension, "unknown"))][row.get("verdict", "invalid")] += 1
        grouped[dimension] = {
            key: {"total": sum(counter.values()), **dict(counter)}
            for key, counter in sorted(buckets.items(), key=lambda item: (-sum(item[1].values()), item[0]))
        }
    noncorrect = [row for row in rows if row.get("verdict") in {"incorrect", "uncertain"}]
    return {**coverage, "group_breakdowns": grouped,
            "noncorrect_task_ids": [row.get("task_id") for row in noncorrect]}, noncorrect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--labels-dir", type=Path, required=True)
    parser.add_argument("--kind", choices=("edges", "nodes"), required=True)
    parser.add_argument("--reviewer-kind", choices=("ai", "human"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result, noncorrect = summarize(args.manifest, args.labels_dir, args.kind, args.reviewer_kind)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8")
    args.out.with_name(args.out.stem + "-noncorrect.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in noncorrect), encoding="utf-8")
    lines = [f"# Full-population {args.kind} review", "",
             f"- Population: {result['population']:,}",
             f"- Valid labels: {result['valid_labels']:,} ({result['coverage']:.2%} coverage)",
             f"- Full population complete: {result['full_population_complete']}",
             f"- Verdicts: {result['verdicts']}",
             f"- Human precision: {result['precision']}",
             f"- AI screen correct share: {result['ai_screen_correct_share']}",
             f"- Interpretation: {result['interpretation']}", "",
             "## Predicate breakdown" if args.kind == "edges" else "## Entity type breakdown", ""]
    primary = "predicate" if args.kind == "edges" else "candidate_type"
    lines += ["| Group | Total | Correct | Incorrect | Uncertain |", "|---|---:|---:|---:|---:|"]
    for name, counts in result["group_breakdowns"][primary].items():
        lines.append(f"| {name} | {counts['total']} | {counts.get('correct', 0)} | "
                     f"{counts.get('incorrect', 0)} | {counts.get('uncertain', 0)} |")
    lines += ["", "AI verdicts cover each listed prediction; they are not independent human gold labels.",
              "A complete review of predicted edges estimates precision for this pinned export, not recall.", ""]
    args.out.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({key: result[key] for key in
                      ("population", "valid_labels", "coverage", "full_population_complete",
                       "verdicts", "precision", "ai_screen_correct_share")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
