#!/usr/bin/env python3
"""Read-only Neo4j AuraDB query runner for the Weconomy report.

Outputs reports/auradb_results.json and reports/auradb_results.md.
No credentials are printed or persisted. Individual failed queries are logged
in reports/auradb_errors.json rather than stopping the run.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase, Query, READ_ACCESS

BASE = Path(__file__).resolve().parent
HEADER = re.compile(r"^//\s+(Q\d+[a-z]?)\s+\[(core|extended|heavy)\]\s*(.*)$", re.I)


def load_neo4j_env():
    """Load Neo4j settings from the nearest .env without overriding the shell."""
    env_file = next((folder / ".env" for folder in (BASE, *BASE.parents)
                     if (folder / ".env").is_file()), None)
    if env_file is None:
        return
    keys = {"NEO4J_URI", "NEO4J_USER", "NEO4J_USERNAME", "NEO4J_PASSWORD", "NEO4J_DATABASE"}
    for line in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.removeprefix("export ").split("=", 1)
        if key.strip() in keys:
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_queries(path: Path):
    current = None
    statements = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADER.match(line)
        if match:
            if current and statements:
                yield (*current, "\n".join(statements).rstrip("; \n"))
            current = (match.group(1), match.group(2).lower(), match.group(3))
            statements = []
        elif current and line.strip() and not line.lstrip().startswith("//"):
            statements.append(line)
    if current and statements:
        yield (*current, "\n".join(statements).rstrip("; \n"))


def serialize(value):
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def main():
    parser = argparse.ArgumentParser(description="Collect read-only AuraDB report metrics")
    parser.add_argument("--level", choices=["core", "extended", "all"], default="core")
    parser.add_argument("--output", default="reports", help="output directory")
    parser.add_argument("--timeout", type=float, default=35, help="per-query timeout in seconds")
    parser.add_argument("--queries", default=str(BASE / "auradb_queries.cypher"))
    parser.add_argument("--only", nargs="*", default=None, help="Run specific Q IDs e.g. Q14 Q27")
    args = parser.parse_args()

    load_neo4j_env()
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER") or os.getenv("NEO4J_USERNAME") or "neo4j"
    password = os.getenv("NEO4J_PASSWORD")
    if not uri or not password:
        parser.error("Set NEO4J_URI and NEO4J_PASSWORD environment variables first")

    levels = {"core": {"core"}, "extended": {"core", "extended"}, "all": {"core", "extended", "heavy"}}
    selected = []
    for qid, level, label, statement in load_queries(Path(args.queries)):
        if not statement.strip() or qid in {"Q59"}:
            continue  # Q59 has placeholder ID and is for Browser visualization only.
        if args.only is not None:
            if qid.upper() not in {x.upper() for x in args.only}:
                continue
        elif level not in levels[args.level]:
            continue
        selected.append((qid, level, label, statement))

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    errors = {}
    try:
        with GraphDatabase.driver(uri, auth=(user, password)) as driver:
            driver.verify_connectivity()
            with driver.session(default_access_mode=READ_ACCESS) as session:
                for qid, level, label, statement in selected:
                    print(f"Running {qid} [{level}] — {label}", flush=True)
                    try:
                        records = session.run(Query(statement, timeout=args.timeout))
                        values = [serialize(rec.data()) for rec in records]
                        results[qid] = {"title": label, "level": level, "rows": values, "row_count": len(values)}
                    except Exception as ex:
                        errors[qid] = {"title": label, "error": f"{type(ex).__name__}: {ex}"}
                        print(f"  skipped/failed: {type(ex).__name__}", file=sys.stderr)
    except Exception as ex:
        parser.error(f"Connection failed: {type(ex).__name__}: {ex}")

    payload = {"generated_utc": datetime.now(timezone.utc).isoformat(),
               "source": "Neo4j AuraDB", "level": args.level,
               "results": results, "errors": errors}
    (out / "auradb_results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "auradb_errors.json").write_text(json.dumps(errors, indent=2, ensure_ascii=False), encoding="utf-8")
    chunks = ["# Weconomy — AuraDB report metrics\n", f"Generated: {payload['generated_utc']}\n"]
    for qid, data in results.items():
        chunks.append(f"## {qid} — {data['title']} ({data['row_count']} rows)\n")
        chunks.append("```json\n" + json.dumps(data["rows"], indent=2, ensure_ascii=False) + "\n```\n")
    if errors:
        chunks.append("## Errors (queries that need review)\n")
        chunks.append("```json\n" + json.dumps(errors, indent=2, ensure_ascii=False) + "\n```\n")
    (out / "auradb_results.md").write_text("\n".join(chunks), encoding="utf-8")
    print(f"Done: {len(results)} queries OK, {len(errors)} failed. Files in: {out.resolve()}")


if __name__ == "__main__":
    main()
