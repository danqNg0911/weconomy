#!/usr/bin/env python3
"""Inspect Hugging Face Weconomy Parquet runs (or a local run) for report statistics.

Works with .parquet files and ZIP run bundles containing .parquet. It produces
inventory, schemas, counts, distinct counts, categorical distributions, date
histograms, and small EXCERPTS (never full article bodies). This script does NOT
know whether separate runs overlap: choose a SINGLE final run for final totals.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import zipfile

import duckdb
import pyarrow.parquet as pq


def qident(s: str) -> str:
    return '"' + s.replace('"', '""') + '"'


def quote(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def safe_extract_parquet_bundles(base: Path, extract_to: Path):
    bundles = sorted(base.rglob("*.zip"))
    extracted = 0
    for bundle in bundles:
        if extract_to in bundle.parents:
            continue
        target_base = extract_to / bundle.relative_to(base).with_suffix("")
        try:
            with zipfile.ZipFile(bundle, "r") as archive:
                for member in archive.infolist():
                    if member.is_dir() or not member.filename.lower().endswith(".parquet"):
                        continue
                    inner = Path(member.filename.replace("\\", "/"))
                    if inner.is_absolute() or ".." in inner.parts:
                        continue
                    target = (target_base / inner).resolve()
                    if not target.is_relative_to(target_base.resolve()):
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.exists() and target.stat().st_size == member.file_size:
                        continue
                    with archive.open(member) as src, target.open("wb") as dst:
                        while chunk := src.read(1024 * 1024):
                            dst.write(chunk)
                    extracted += 1
        except (zipfile.BadZipFile, OSError) as ex:
            print(f"Cannot read {bundle}: {ex}")
    print(f"ZIP bundles inspected: {len(bundles)}, extracted parquet: {extracted}")


def table_name(path: Path) -> str:
    known = {"bronze", "articles", "sentences", "mentions", "entities", "relations", "events", "claims"}
    stem = path.stem.lower()
    if stem in known:
        return stem
    for part in [path.parent.name.lower(), path.parent.parent.name.lower()]:
        if part in known:
            return part
    return stem


def view_expr(paths: list[Path]) -> str:
    return "read_parquet([" + ",".join(quote(str(p.resolve())) for p in paths) + "], union_by_name=true)"


def main():
    ap = argparse.ArgumentParser(description="Inventory and aggregate HF Weconomy Parquet")
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--repo", help="HF repo id, e.g. ORG/weconomy-dataset")
    source.add_argument("--local", help="Existing downloaded run or dataset folder")
    ap.add_argument("--revision", default=None, help="HF branch/tag/commit, default main")
    ap.add_argument("--subdir", default=None, help="Optional subdirectory for ONE final run")
    ap.add_argument("--download-to", default="hf_snapshot", help="Local HF dataset cache")
    ap.add_argument("--output", default="reports", help="Summary output folder")
    ap.add_argument("--no-extract-zip", action="store_true", help="Do not inspect zip bundles")
    ap.add_argument("--schema-only", action="store_true", help="Fast file+row+schema inventory, skip GROUP BY")
    args = ap.parse_args()

    if args.repo:
        from huggingface_hub import snapshot_download
        print("Downloading/indexing HF dataset snapshot; login with 'hf auth login' for private repositories.")
        folder = Path(snapshot_download(
            repo_id=args.repo, repo_type="dataset", revision=args.revision,
            local_dir=args.download_to,
            allow_patterns=["*.parquet", "*.zip", "*.json", "*.jsonl", "*.md"],
        ))
    else:
        folder = Path(args.local).expanduser().resolve()
    if not folder.is_dir():
        ap.error(f"Folder not found: {folder}")

    # Extract under the chosen snapshot root to preserve the original provenance.
    if not args.no_extract_zip:
        safe_extract_parquet_bundles(folder, folder / "_extracted_parquet_bundles")

    selected = (folder / args.subdir).resolve() if args.subdir else folder.resolve()
    if not selected.is_dir() or not selected.is_relative_to(folder.resolve()):
        ap.error("--subdir must be an existing directory inside the snapshot")

    parquet_files = sorted(selected.rglob("*.parquet"))
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if not parquet_files:
        print("No Parquet discovered. Check zip bundles or selection path.")
        return

    inventory = []
    groups = defaultdict(list)
    for p in parquet_files:
        try:
            pf = pq.ParquetFile(p)
            schema = pf.schema_arrow
            t = table_name(p)
            groups[t].append(p)
            inventory.append({"path": str(p.relative_to(folder)), "table": t,
                              "rows": pf.metadata.num_rows, "bytes": p.stat().st_size,
                              "columns": {field.name: str(field.type) for field in schema}})
        except Exception as ex:
            inventory.append({"path": str(p.relative_to(folder)), "error": str(ex)})

    output = {"generated_utc": datetime.now(timezone.utc).isoformat(),
              "repo": args.repo, "revision": args.revision, "folder": str(folder),
              "selected_subdir": args.subdir,
              "IMPORTANT": "Counts from multiple stored runs can overlap. Select ONE final run to report totals.",
              "inventory": inventory, "tables": {}}
    connection = duckdb.connect(database=":memory:")
    categories = ["source_id", "source", "host", "domain", "language", "lang", "status",
                  "decision", "duplicate_status", "quality_status", "predicate", "entity_type",
                  "relation_type", "type", "review_status", "polarity", "method", "model", "label"]
    identifiers = ["article_id", "document_id", "entity_id", "relation_id", "claim_id", "event_id",
                   "sentence_id", "mention_id", "source_url", "canonical_url", "url", "checksum"]
    dates = ["published_at", "published_date", "publication_date", "published", "collected_at", "fetched_at"]
    examples = ["article_id", "title", "source_id", "language", "entity_id", "canonical_name", "name",
                "type", "predicate", "subject_id", "object_id", "subject_entity_id", "object_entity_id",
                "event_id", "sentence_id", "evidence"]
    for table, paths in sorted(groups.items()):
        print(f"Inspecting {table}: {len(paths)} file(s)", flush=True)
        source_expr = view_expr(paths)
        info = {"file_count": len(paths), "paths": [str(p.relative_to(folder)) for p in paths]}
        try:
            desc = connection.execute(f"DESCRIBE SELECT * FROM {source_expr}").fetchall()
            columns = {row[0]: row[1] for row in desc}
            info["columns"] = columns
            info["rows"] = connection.execute(f"SELECT COUNT(*) FROM {source_expr}").fetchone()[0]
            if not args.schema_only:
                info["identifiers"] = {}
                for key in identifiers:
                    if key not in columns:
                        continue
                    key_sql = qident(key)
                    row = connection.execute(
                        f"SELECT COUNT(*) FILTER (WHERE {key_sql} IS NOT NULL), "
                        f"COUNT(DISTINCT {key_sql}) FROM {source_expr}").fetchone()
                    info["identifiers"][key] = {"non_null": row[0], "distinct": row[1]}
                info["top_values"] = {}
                for key in categories:
                    if key not in columns or any(x in columns[key].upper() for x in ("[]", "STRUCT", "MAP")):
                        continue
                    name = qident(key)
                    try:
                        rows = connection.execute(
                            f"SELECT LEFT(CAST({name} AS VARCHAR),150) AS val, COUNT(*) AS n "
                            f"FROM {source_expr} GROUP BY 1 ORDER BY n DESC LIMIT 35").fetchall()
                        info["top_values"][key] = [{"value": k, "count": c} for k, c in rows]
                    except Exception as ex:
                        info["top_values"][key] = {"error": str(ex)}
                # Text-length and per-document structural statistics, where schema supports them.
                if table == "articles":
                    text_col = next((x for x in ["text", "body_text", "body", "content", "clean_text", "article_text"]
                                     if x in columns and ("VARCHAR" in columns[x].upper() or "STRING" in columns[x].upper())), None)
                    if text_col:
                        name = qident(text_col)
                        r = connection.execute(
                            f"SELECT MIN(LENGTH({name})), AVG(LENGTH({name})), "
                            f"MEDIAN(LENGTH({name})), MAX(LENGTH({name})), "
                            f"COUNT(*) FILTER (WHERE {name} IS NULL OR LENGTH(TRIM({name}))=0) "
                            f"FROM {source_expr}").fetchone()
                        info["body_length_chars"] = {"column":text_col, "min":r[0], "mean":r[1],
                                                     "median":r[2], "max":r[3], "empty_or_null":r[4]}
                    if "source_id" in columns and "language" in columns:
                        rows = connection.execute(
                            f"SELECT CAST(source_id AS VARCHAR), CAST(language AS VARCHAR), COUNT(*) "
                            f"FROM {source_expr} GROUP BY 1,2 ORDER BY 3 DESC LIMIT 100").fetchall()
                        info["source_by_language"] = [{"source_id":a,"language":b,"articles":n} for a,b,n in rows]
                if table in {"mentions", "sentences", "relations", "events"}:
                    docid = next((x for x in ["article_id", "document_id"] if x in columns),None)
                    if docid:
                        key = qident(docid)
                        res = connection.execute(
                            f"SELECT COUNT(*) AS articles, AVG(n), MEDIAN(n), MAX(n) FROM "
                            f"(SELECT {key},COUNT(*) AS n FROM {source_expr} "
                            f"WHERE {key} IS NOT NULL GROUP BY {key})").fetchone()
                        info["per_document"] = {"key":docid,"documents_with_rows":res[0],
                                                "mean":res[1],"median":res[2],"max":res[3]}
                info["years"] = {}
                for key in dates:
                    if key not in columns:
                        continue
                    name = qident(key)
                    try:
                        rows = connection.execute(
                            f"SELECT YEAR(TRY_CAST({name} AS TIMESTAMP)) AS year, COUNT(*) AS n "
                            f"FROM {source_expr} GROUP BY 1 ORDER BY year").fetchall()
                        info["years"][key] = [{"year": y, "count": n} for y,n in rows]
                    except Exception as ex:
                        info["years"][key] = {"error": str(ex)}
                sample_cols = [k for k in examples if k in columns]
                if sample_cols:
                    select = ", ".join(f"LEFT(CAST({qident(k)} AS VARCHAR),180) AS {qident(k)}" for k in sample_cols)
                    rows = connection.execute(f"SELECT {select} FROM {source_expr} ORDER BY random() LIMIT 8").fetchall()
                    info["examples"] = [dict(zip(sample_cols, row)) for row in rows]
        except Exception as ex:
            info["error"] = f"{type(ex).__name__}: {ex}"
        output["tables"][table] = info

    write_json(out / "hf_parquet_summary.json", output)
    lines = ["# Weconomy — Hugging Face Parquet statistics",
             "", f"Run selection: `{args.subdir or '(entire folder)'}`", "",
             "**Important:** Do not add counts from overlapping runs as if they are unique articles.\n",
             "| Table | Parquet files | Rows |", "|---|---:|---:|"]
    for t, val in output["tables"].items():
        lines.append(f"| {t} | {val['file_count']} | {val.get('rows', 'ERROR')} |")
    for t, val in output["tables"].items():
        lines.extend([f"\n## {t}", "", "```json", json.dumps(val, ensure_ascii=False, indent=2, default=str), "```"])
    (out / "hf_parquet_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Saved:", out.resolve() / "hf_parquet_summary.json")
    print("Do not send HF auth tokens; this output contains only data statistics and short excerpts.")


if __name__ == "__main__":
    main()
