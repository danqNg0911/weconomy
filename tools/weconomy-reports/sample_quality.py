#!/usr/bin/env python3
"""Create a stratified review sample of claims; or evaluate human labels.

Accuracy/precision above 90% CANNOT be established from raw output counts.
Positive-only sampling estimates precision of extracted claims, NOT recall.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from collections import defaultdict


def evaluate(path: Path):
    grouped = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            label = (r.get("is_correct", "") or "").strip().lower()
            if label in {"1", "true", "yes", "đúng", "dung"}:
                v = 1
            elif label in {"0", "false", "no", "sai"}:
                v = 0
            else:
                continue
            grouped["ALL"].append(v)
            grouped[r.get("predicate", "UNKNOWN")].append(v)
    print("label / n / correct / precision / Wilson 95% CI")
    for name, labels in sorted(grouped.items(), key=lambda kv: (kv[0] != "ALL", kv[0])):
        n = len(labels)
        if not n:
            continue
        p = sum(labels)/n
        z = 1.96
        den = 1+z*z/n
        center = (p+z*z/(2*n))/den
        width = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
        print(f"{name}: n={n}, correct={sum(labels)}, precision={p:.4%}, Wilson95%=[{max(0,center-width):.4%},{min(1,center+width):.4%}]")
    print("Recall and F1 require a separately annotated ground-truth set INCLUDING missed relations.")


def generate(folder: Path, out: Path, per_type: int):
    import duckdb
    paths = sorted(folder.rglob("relations.parquet"))
    if not paths:
        raise SystemExit("No relations.parquet files. Select a final run directory with --local.")
    print(f"Found {len(paths)} relation files. Ensure no overlapping historic runs are included.")
    qpath = lambda p: "'"+str(p.resolve()).replace("'","''")+"'"
    src = "read_parquet(["+",".join(qpath(p) for p in paths)+"], union_by_name=true)"
    conn = duckdb.connect()
    cols = [r[0] for r in conn.execute(f"DESCRIBE SELECT * FROM {src}").fetchall()]
    def choose(*names):
        return next((x for x in names if x in cols), None)
    columns = {
        "predicate":choose("predicate","relation_type"),
        "subject_id":choose("subject_id","subject_entity_id","source_id","head_id","from_id"),
        "object_id":choose("object_id","object_entity_id","target_id","tail_id","to_id"),
        "evidence":choose("evidence","evidence_text","sentence_text","sentence"),
        "document_id":choose("document_id","article_id","document_ids"),
        "event_id":choose("event_id"),
        "source":choose("source_ids","source_id","url","source_url"),
        "review_status":choose("review_status"),
    }
    if not columns["predicate"]:
        raise SystemExit(f"No predicate column in relations files. Available columns: {cols}")
    qident = lambda s: '"'+s.replace('"','""')+'"'
    sql_cols=[]
    for alias, name in columns.items():
        expression = f"left(CAST({qident(name)} AS VARCHAR),900)" if name else "NULL::VARCHAR"
        sql_cols.append(f"{expression} AS {qident(alias)}")
    pcol = qident(columns["predicate"])
    query = ("SELECT "+", ".join(qident(x) for x in columns)+" FROM (SELECT "+", ".join(sql_cols)+
             f", row_number() OVER (PARTITION BY {pcol} ORDER BY random()) AS rn "
             f"FROM {src} WHERE {pcol} IS NOT NULL) q WHERE rn <= {per_type} "
             "ORDER BY predicate, rn")
    rows = conn.execute(query).fetchall()
    headers = list(columns)+["is_correct", "error_type", "reviewer_notes"]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            d = dict(zip(columns,row))
            d.update({"is_correct":"", "error_type":"", "reviewer_notes":""})
            writer.writerow(d)
    print(f"Saved {len(rows)} samples to {out}")
    print("Annotate is_correct = 1 only if subject, predicate, object AND evidence are correct; otherwise 0.")
    print(f"Run: python sample_quality.py --evaluate \"{out}\"")


def main():
    parser = argparse.ArgumentParser(description="Stratified claims annotation and evaluation")
    parser.add_argument("--local", help="folder of ONE final run containing relations.parquet")
    parser.add_argument("--per-predicate", type=int, default=15)
    parser.add_argument("--out", default="reports/annotation_sample.csv")
    parser.add_argument("--evaluate", help="CSV with is_correct labels, 0 or 1")
    args = parser.parse_args()
    if args.evaluate:
        evaluate(Path(args.evaluate))
    elif args.local:
        generate(Path(args.local), Path(args.out), args.per_predicate)
    else:
        parser.error("Provide --local FOLDER or --evaluate CSV")


if __name__ == "__main__":
    main()
