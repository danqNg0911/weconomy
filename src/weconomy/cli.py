import argparse
import json
import sys
from pathlib import Path

from .access import Access, katana_urls
from .analytics import analyze
from .graph import import_graph
from .pipeline import load_config, process
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
    run.add_argument("--ner", choices=["gazetteer", "models"])
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
    args = parser.parse_args()
    code = 0
    try:
        if args.command == "schema":
            result = {"tables": {key: str(value) for key, value in SCHEMAS.items()},
                      "relations": RELATION_TYPES}
        elif args.command in {"run", "discover"}:
            config = load_config(args.config)
            if args.command == "run":
                if args.ner:
                    config["ner_backend"] = args.ner
                run, report = process(config, manifest=args.manifest,
                                      urls=katana_urls(args.urls) if args.urls else None)
                result = {"run": str(run), **report}
                code = int(bool(report["errors"]))
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
        if getattr(args, "output", None) and args.command in {"analytics", "evaluate"}:
            write_new_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return code
    except Exception as exc:
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
