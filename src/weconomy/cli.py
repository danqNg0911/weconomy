import argparse
import json
import sys
from pathlib import Path

from .access import Access, katana_urls
from .analytics import analyze
from .graph import import_graph
from .hub import pull_run, push_run
from .pipeline import load_config, process, read_table
from .quality import annotation_tasks, evaluate, validate, write_new_json
from .schema import RELATION_TYPES, SCHEMAS


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Evidence-first news knowledge graph")
    parser.add_argument("--config", default="config/pipeline.yaml")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Process licensed local snapshots or permitted article URLs")
    inputs = run.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--manifest", type=Path)
    inputs.add_argument("--urls", type=Path, help="URL lines or Katana JSONL; still checked against policy")
    inputs.add_argument("--from-run", type=Path, help="Reprocess saved bronze HTML without network requests")
    run.add_argument("--ner", choices=["gazetteer", "models"])
    run.add_argument("--allow-excerpts", action="store_true", help="Diagnostic NLP on declared excerpts only")
    collect = sub.add_parser("collect", help="RSS -> full article body checks -> NER/relations -> immutable run")
    collect.add_argument("--source", action="append", required=True, help="Repeat for multiple sources")
    collect.add_argument("--limit", type=int, default=3, help="Maximum article URLs attempted per source")
    collect.add_argument("--ner", choices=["gazetteer", "models"], default="models")
    collect.add_argument("--skip-run", type=Path, action="append", default=[],
                         help="Skip URLs already accepted as full text in this run; repeat as needed")
    merge = sub.add_parser("merge-runs", help="Reprocess and deduplicate accepted full-text snapshots offline")
    merge.add_argument("--run", dest="runs", type=Path, action="append", required=True,
                       help="Repeat in revision preference order; last accepted capture of each URL wins")
    merge.add_argument("--ner", choices=["gazetteer", "models"], default="models")
    export = sub.add_parser("export", help="Export a run table as UTF-8 JSONL")
    export.add_argument("run", type=Path)
    export.add_argument("--table", choices=["articles", "sentences", "mentions", "entities", "relations", "events"],
                        required=True)
    export.add_argument("--output", type=Path, required=True)
    discovery = sub.add_parser("discover")
    discovery.add_argument("source")
    discovery.add_argument("--limit", type=int, default=10)
    discovery.add_argument("--output", type=Path, required=True)
    for name in ("validate", "analytics", "import-neo4j", "label-tasks", "evaluate"):
        p = sub.add_parser(name)
        p.add_argument("run", type=Path)
        if name == "analytics":
            p.add_argument("--small-world", action="store_true")
        if name == "label-tasks":
            p.add_argument("--output", type=Path, required=True)
            p.add_argument("--limit", type=int, default=200)
        if name == "evaluate":
            p.add_argument("--labels", type=Path, required=True)
        if name in {"evaluate", "analytics"}:
            p.add_argument("--output", type=Path)
    sub.add_parser("schema")
    push = sub.add_parser("hf-push", help="Upload a validated run bundle to a private HF dataset repo")
    push.add_argument("run", type=Path)
    push.add_argument("--repo", required=True, help="Hugging Face dataset namespace/name")
    push.add_argument("--dry-run", action="store_true", help="Validate and preview bundle without network")
    pull = sub.add_parser("hf-pull", help="Download and validate a versioned HF run without overwriting")
    pull.add_argument("--repo", required=True)
    pull.add_argument("--run-id", required=True)
    pull.add_argument("--revision", default="main", help="Commit SHA recommended for reproducibility")
    pull.add_argument("--output", type=Path, default=Path("data/runs"), help="Local parent directory")
    args = parser.parse_args()
    code = 0
    try:
        if args.command == "hf-push":
            result = push_run(args.run, args.repo, dry_run=args.dry_run)
        elif args.command == "hf-pull":
            result = pull_run(args.repo, args.run_id, args.output, revision=args.revision)
        elif args.command == "schema":
            result = {"tables": {key: str(value) for key, value in SCHEMAS.items()},
                      "relations": RELATION_TYPES}
        elif args.command in {"run", "collect", "discover", "merge-runs"}:
            config = load_config(args.config)
            if args.command in {"run", "collect", "merge-runs"}:
                if args.ner:
                    config["ner_backend"] = args.ner
                if args.command == "collect":
                    run, report = process(config, sources=args.source, limit_per_source=args.limit,
                                          skip_runs=args.skip_run)
                elif args.command == "merge-runs":
                    run, report = process(config, from_runs=args.runs)
                else:
                    config["allow_excerpts"] = args.allow_excerpts
                    run, report = process(config, manifest=args.manifest, from_run=args.from_run,
                                          urls=katana_urls(args.urls) if args.urls else None)
                result = {"run": str(run), **report}
                code = int(report["status"] not in {"completed", "no_new_documents"})
            else:
                if args.limit <= 0 or args.limit > config["max_documents"]:
                    raise ValueError("Discovery limit must be within configured document budget")
                access = Access(config)
                try:
                    urls = access.discover(args.source, args.limit)
                finally:
                    access.close()
                with args.output.open("x", encoding="utf-8") as stream:
                    stream.write("\n".join(urls) + "\n")
                result = {"urls": len(urls), "output": str(args.output)}
        elif args.command == "validate":
            result = validate(args.run)
            code = int(not result["valid"])
        elif args.command == "analytics":
            result = analyze(args.run, small_world=args.small_world)
        elif args.command == "label-tasks":
            if args.limit <= 0:
                raise ValueError("Label task limit must be positive")
            result = annotation_tasks(args.run, args.output, args.limit)
        elif args.command == "evaluate":
            result = evaluate(args.run, args.labels)
        elif args.command == "import-neo4j":
            result = import_graph(args.run)
        elif args.command == "export":
            rows = read_table(args.run, args.table)
            with args.output.open("x", encoding="utf-8") as stream:
                for row in rows:
                    stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
            result = {"rows": len(rows), "table": args.table, "output": str(args.output)}
        if getattr(args, "output", None) and args.command in {"analytics", "evaluate"}:
            write_new_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return code
    except Exception as exc:
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
