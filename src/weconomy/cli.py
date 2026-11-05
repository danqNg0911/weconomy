import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from uuid import uuid4

from .access import katana_urls
from .analytics import analyze
from .crawler import run_collection
from .dataset import collect_dataset, dataset_status, export_dataset, validate_dataset_resume
from .graph import import_graph
from .hub import pull_run, push_run
from .pipeline import load_config, process, read_table
from .quality import annotation_tasks, evaluate, validate, write_new_json
from .schema import RELATION_TYPES, SCHEMAS
from .sources import source_status

_DEFAULT_DATASET = Path("data/datasets/international-business-katana")
_DEFAULT_EXPORT = Path("data/exports/international-business-katana")
_STATUS_LINE = ""
_STATUS_LOCK = Lock()


def _unique_output_path(path):
    path = Path(path)
    if not path.exists():
        return path
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    while True:
        candidate = path.with_name(f"{path.name}-{stamp}-{uuid4().hex[:8]}")
        if not candidate.exists():
            return candidate


def _write_progress(message, event):
    with _STATUS_LOCK:
        _write_progress_locked(message, event)


def _write_progress_locked(message, event):
    global _STATUS_LINE
    stream = sys.stderr
    name = event.get("event")
    error = name in {"error", "pagination_error"} or event.get("status") == "error"
    color = "\x1b[1;31m" if error else ""
    reset = "\x1b[0m" if color else ""
    if not stream.isatty():
        if name != "finished":
            print(f"[weconomy] {message}", file=stream, flush=True)
        return
    if name in {"article_start", "heartbeat", "models_loading", "dataset_batch_start"}:
        if name == "article_start":
            total = max(1, event.get("total", 1))
            percent = min(99, int((event.get("index", 1) - 1) * 100 / total))
            blocks = percent // 5
            message = f"[{percent:2}%] [{'█' * blocks}{'░' * (20 - blocks)}] {message}"
        _STATUS_LINE = f"[weconomy] {message}"
        stream.write(f"\r\x1b[2K{_STATUS_LINE}")
        stream.flush()
        return
    if name == "finished":
        stream.write("\r\x1b[2K")
        stream.write(f"\x1b[1;32m[weconomy] [100%] Hoàn tất: {message}\x1b[0m\n")
        stream.flush()
        _STATUS_LINE = ""
        return
    stream.write("\r\x1b[2K")
    stream.write(f"{color}[weconomy] {message}{reset}\n")
    if name == "article_done" and event.get("total"):
        total = max(1, event["total"])
        percent = min(99, int(event.get("index", 1) * 100 / total))
        blocks = percent // 5
        _STATUS_LINE = (f"[weconomy] [{percent:2}%] [{'█' * blocks}{'░' * (20 - blocks)}] "
                        f"{event.get('stage', 'crawl')}: {event.get('index', 0)}/{total}")
    if _STATUS_LINE:
        stream.write(_STATUS_LINE)
    stream.flush()


def _console_progress(event):
    name = event.get("event")
    stage = event.get("stage", "crawl")
    if name == "target_start":
        message = f"[{event['index']}/{event['total']}] Target {event['target']}: khám phá {event['url']}"
    elif name == "katana_start":
        message = f"Katana bắt đầu crawl: {event['url']}"
    elif name == "category_page":
        message = (f"Target {event['target']}: trang danh mục {event['page']} — "
                   f"+{event['new_articles']} bài (tổng {event['total_articles']})")
    elif name == "pagination_error":
        message = f"Target {event['target']}: lỗi trang tiếp theo {event['url']}: {event['error']}"
    elif name == "target_discovered":
        message = f"Target {event['target']}: tìm thấy {event['count']} URL bài"
    elif name == "batch_start":
        message = (f"Target {event['target']}: xử lý batch {event['index']} "
                   f"({event['size']} bài; {event['attempted']}/{event['cap']} URL)")
    elif name == "article_start":
        message = f"{stage}: [{event['index']}/{event['total']}] đang tải/xử lý {event['url']}"
    elif name == "article_done":
        detail = event.get("error") or event.get("title", "")
        if event.get("error_type"):
            detail = f"{event['error_type']}: {detail}"
        counts = (f" | {event.get('entities', 0)} entity, {event.get('relations', 0)} relation"
                  if "entities" in event else "")
        content = (f" | {event['word_count']} từ, {event['body_paragraphs']} đoạn, "
                   f"{event['nlp_sentences']} câu NLP" if "word_count" in event else "")
        message = (f"{stage}: [{event['index']}/{event['total']}] {event['status']} "
                   f"{detail}{counts}{content}").rstrip()
    elif name == "batch_done":
        counts = event["counts"]
        message = (f"Target {event['target']}: batch {event['index']} xong — "
                   f"{counts['articles']} bài, {counts['nodes']} node, "
                   f"{counts['relations']} cạnh, {counts['relation_types']} loại")
    elif name == "dataset_replay_start":
        message = f"Bắt đầu phát lại {event['runs']} run đã lưu vào dataset {event['dataset']}"
    elif name == "models_loading":
        message = "Đang nạp mô hình NLP"
    elif name == "dataset_batch_start":
        message = (f"Dataset: nạp batch {event['size']} bài "
                   f"({event['allocated']}/{event['budget']} URL đã phân bổ)")
    elif name == "dataset_batch_done":
        counts = event["counts"]
        message = (f"Dataset hiện có {counts['articles']} bài, {counts['nodes']} node, "
                   f"{counts['relations']} cạnh, {counts['relation_types']} loại")
    elif name == "heartbeat":
        message = f"{event['message']} ({event['elapsed_seconds']} giây)"
    elif name == "error":
        context = f"batch {event.get('batch')} " if event.get("batch") else ""
        message = (f"LỖI {event.get('stage', 'weconomy')} {context}"
                   f"{event.get('error_type', 'Error')}: {event.get('error', 'Không rõ nguyên nhân')}")
    elif name == "info":
        message = event["message"]
    elif name == "finished":
        message = event.get("status", "tác vụ đã kết thúc")
    else:
        return
    _write_progress(message, event)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Evidence-first news knowledge graph")
    parser.add_argument("--config", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    crawl = sub.add_parser("crawl", help="Run bounded Katana discovery and process article batches")
    crawl.add_argument("--config", type=Path, default=Path("config/collection.yaml"))
    crawl.add_argument("--target", action="append", dest="targets", help="Target ID; repeat to select multiple")
    collect = sub.add_parser("collect", help="Crawl with Katana and add the results to the default dataset")
    collect.add_argument("--config", type=Path, default=Path("config/collection.yaml"))
    collect.add_argument("--target", action="append", dest="targets", help="Target ID; repeat to select multiple")
    collect.add_argument("--dataset", type=Path, default=_DEFAULT_DATASET)
    collect.add_argument("--articles", type=int)
    collect.add_argument("--nodes", type=int, default=2000)
    collect.add_argument("--relations", type=int, default=5000)
    collect.add_argument("--relation-types", type=int, default=11)
    collect.add_argument("--max-candidates", type=int, default=10000)
    collect.add_argument("--batch-size", type=int, default=20)
    collect_mode = collect.add_mutually_exclusive_group()
    collect_mode.add_argument("--resume", action="store_true")
    collect_mode.add_argument("--force", action="store_true",
                              help="Create a new uniquely named dataset beside an existing one")
    run = sub.add_parser("run", help="Process licensed local snapshots or permitted article URLs")
    inputs = run.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--manifest", type=Path)
    inputs.add_argument("--urls", type=Path, help="URL lines or Katana JSONL; still checked against policy")
    inputs.add_argument("--from-run", type=Path, help="Reprocess saved bronze HTML without network requests")
    run.add_argument("--ner", choices=["gazetteer", "models"])
    run.add_argument("--allow-excerpts", action="store_true", help="Diagnostic NLP on declared excerpts only")
    dataset_collect = sub.add_parser("collect-dataset", help="Collect a resumable, persistent topic dataset")
    dataset_collect.add_argument("--dataset", type=Path, default=_DEFAULT_DATASET)
    dataset_inputs = dataset_collect.add_mutually_exclusive_group(required=True)
    dataset_inputs.add_argument("--urls", type=Path, help="File containing one article URL per line")
    dataset_inputs.add_argument("--from-run", type=Path, action="append", dest="from_runs",
                                help="Replay eligible full-page bodies from a saved run; repeat in preference order")
    for name in ("articles", "nodes", "relations", "relation-types"):
        dataset_collect.add_argument(f"--{name}", type=int, dest=name.replace("-", "_"))
    dataset_collect.add_argument("--max-candidates", type=int, default=1000)
    dataset_collect.add_argument("--batch-size", type=int, default=20)
    dataset_mode = dataset_collect.add_mutually_exclusive_group()
    dataset_mode.add_argument("--resume", action="store_true")
    dataset_mode.add_argument("--force", action="store_true",
                              help="Create a new uniquely named dataset beside an existing one")
    dataset_collect.add_argument("--ner", choices=["gazetteer", "models"])
    status = sub.add_parser("dataset-status", help="Show persisted dataset counts and collection state")
    status.add_argument("dataset", type=Path, nargs="?", default=_DEFAULT_DATASET)
    dataset_export = sub.add_parser("export-dataset", help="Export committed dataset tables as JSONL")
    dataset_export.add_argument("dataset", type=Path, nargs="?", default=_DEFAULT_DATASET)
    dataset_export.add_argument("--output", type=Path, default=_DEFAULT_EXPORT)
    sources = sub.add_parser("sources", help="Show configured sources or probe one page per source")
    sources.add_argument("--check", action="store_true")
    sources.add_argument("--source", action="append", dest="source_ids")
    merge = sub.add_parser("merge-runs", help="Reprocess and deduplicate accepted full-text snapshots offline")
    merge.add_argument("--run", dest="runs", type=Path, action="append", required=True,
                       help="Repeat in revision preference order; last accepted capture of each URL wins")
    merge.add_argument("--ner", choices=["gazetteer", "models"], default="models")
    export = sub.add_parser("export", help="Export a run table as UTF-8 JSONL")
    export.add_argument("run", type=Path)
    export.add_argument("--table", choices=["articles", "sentences", "mentions", "entities", "relations", "events"],
                        required=True)
    export.add_argument("--output", type=Path, required=True)
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
    args = parser.parse_args(argv)
    code = 0
    try:
        collection_config = None
        if args.command in {"collect", "collect-dataset"}:
            if args.force:
                previous = args.dataset
                args.dataset = _unique_output_path(args.dataset)
                if args.dataset != previous:
                    _console_progress({"event": "info", "message":
                                       f"Giữ dataset cũ; tạo dataset mới tại {args.dataset}"})
            elif args.dataset.exists() and not args.resume:
                raise FileExistsError(f"Dataset đã tồn tại: {args.dataset}; dùng --resume hoặc --force")
            elif args.resume and not args.dataset.exists():
                raise FileNotFoundError(f"Không tìm thấy dataset để resume: {args.dataset}")
            if args.command == "collect-dataset":
                collection_config = load_config(args.config or "config/collection.yaml")
                if args.ner:
                    collection_config["ner_backend"] = args.ner
            elif args.resume:
                collection_config = load_config(args.config)
            if args.resume:
                validate_dataset_resume(collection_config, args.dataset)
        if args.command == "crawl":
            result = run_collection(args.config, target_ids=args.targets, progress=_console_progress)
            code = int(result["status"] != "completed")
        elif args.command == "collect":
            crawl = run_collection(args.config, target_ids=args.targets, progress=_console_progress)
            from_runs = [Path(run) for target in crawl["targets"] for run in target["run_ids"]]
            if not from_runs:
                result = {"status": "failed", "crawl": crawl, "dataset": None}
                code = 1
            else:
                config = collection_config or load_config(args.config)
                _console_progress({"event": "dataset_replay_start", "runs": len(from_runs),
                                   "dataset": args.dataset})
                dataset = collect_dataset(
                    config, args.dataset, from_runs=from_runs, articles=args.articles,
                    nodes=args.nodes, relations=args.relations, relation_types=args.relation_types,
                    max_candidates=args.max_candidates, batch_size=args.batch_size, resume=args.resume,
                    progress=_console_progress,
                )
                code = (1 if dataset.get("errors") else
                        2 if not dataset["targets_met"] or crawl["status"] != "completed" else 0)
                result = {"status": "completed" if code == 0 else "partial",
                          "crawl": crawl, "dataset": dataset}
        elif args.command == "hf-push":
            result = push_run(args.run, args.repo, dry_run=args.dry_run)
        elif args.command == "hf-pull":
            result = pull_run(args.repo, args.run_id, args.output, revision=args.revision)
        elif args.command == "schema":
            result = {"tables": {key: str(value) for key, value in SCHEMAS.items()},
                      "relations": RELATION_TYPES}
        elif args.command in {"run", "merge-runs", "collect-dataset", "sources"}:
            default_config = "config/collection.yaml" if args.command == "collect-dataset" else "config/pipeline.yaml"
            config = collection_config or load_config(args.config or default_config)
            if args.command in {"run", "merge-runs"}:
                if args.ner:
                    config["ner_backend"] = args.ner
                if args.command == "merge-runs":
                    run, report = process(config, from_runs=args.runs, progress=_console_progress)
                else:
                    config["allow_excerpts"] = args.allow_excerpts
                    run, report = process(config, manifest=args.manifest, from_run=args.from_run,
                                          urls=katana_urls(args.urls) if args.urls else None,
                                          progress=_console_progress)
                result = {"run": str(run), **report}
                code = int(report["status"] not in {"completed", "no_new_documents"})
            elif args.command == "collect-dataset":
                urls = ([line.strip() for line in args.urls.read_text(encoding="utf-8-sig").splitlines()
                         if line.strip()] if args.urls else None)
                result = collect_dataset(
                    config, args.dataset, urls=urls, articles=args.articles,
                    nodes=args.nodes, relations=args.relations, relation_types=args.relation_types,
                    max_candidates=args.max_candidates, batch_size=args.batch_size, resume=args.resume,
                    from_runs=args.from_runs, progress=_console_progress,
                )
                if result.get("errors"):
                    code = 1
                elif any((args.articles, args.nodes, args.relations, args.relation_types)) and not result.get("targets_met"):
                    code = 2
            elif args.command == "sources":
                result = source_status(config, check=args.check, source_ids=args.source_ids)
        elif args.command == "dataset-status":
            result = dataset_status(args.dataset)
        elif args.command == "export-dataset":
            output = _unique_output_path(args.output)
            if output != args.output:
                _console_progress({"event": "info", "message":
                                   f"Giữ bản export cũ; ghi bản mới tại {output}"})
            result = export_dataset(args.dataset, output)
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
        _console_progress({"event": "finished", "status":
                           result.get("status", result.get("reason", "tác vụ đã kết thúc"))})
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return code
    except Exception as exc:
        _console_progress({"event": "error", "stage": args.command,
                           "error_type": type(exc).__name__, "error": str(exc)})
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
