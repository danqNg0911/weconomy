"""Bounded collection, domain normalization, and graph publication cycle."""
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .crawler import run_collection
from .dataset import collect_dataset, dataset_status, export_dataset, validate_dataset_resume
from .domain_filter import filter_domain_export
from .graph import import_graph
from .pipeline import load_config


def _replay_runs(dataset):
    catalog = Path(dataset) / "catalog.sqlite3"
    if not catalog.is_file():
        return []
    uri = catalog.resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as conn:
        return [Path(row[0]) for row in conn.execute(
            "SELECT source_run FROM replay_archives ORDER BY source_run")]


def _output_path(dataset, kind):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return Path("data/exports") / f"{Path(dataset).name}-{kind}-{stamp}-{uuid4().hex[:6]}"


def _load_neo4j_env():
    env_file = Path(".env")
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in {"NEO4J_URI", "NEO4J_USERNAME", "NEO4J_USER", "NEO4J_PASSWORD", "NEO4J_DATABASE"}:
            os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def graph_cycle(dataset, *, config_path=Path("config/collection.yaml"), target_ids=None,
                nodes=2000, relations=5000, relation_types=11, max_candidates=10000,
                batch_size=20, progress=None):
    """Run one bounded collect-normalize-check-publish cycle on an existing dataset."""
    if any(value <= 0 for value in (nodes, relations, relation_types, max_candidates, batch_size)):
        raise ValueError("Targets, candidate budget, and batch size must be positive")
    dataset = Path(dataset)
    if not (dataset / "catalog.sqlite3").is_file():
        raise FileNotFoundError(f"Initialize the dataset first: {dataset}")
    config = load_config(config_path)
    validate_dataset_resume(config, dataset)
    before = dataset_status(dataset)

    if progress:
        progress({"event": "info", "message": "Crawling configured targets for new article URLs"})
    crawl = run_collection(config_path, target_ids=target_ids, progress=progress)
    runs = _replay_runs(dataset)
    for target in crawl.get("targets", []):
        runs.extend(Path(run) for run in target.get("run_ids", []))
    runs = list(dict.fromkeys(runs))

    article_target = before["counts"]["articles"] + int(config["max_articles"])
    candidate_budget = before["attempts_allocated"] + max_candidates
    collect_result = collect_dataset(
        config, dataset, urls=[] if not runs else None, from_runs=runs or None,
        articles=article_target, nodes=nodes, relations=relations, relation_types=relation_types,
        max_candidates=candidate_budget, batch_size=batch_size, resume=True, progress=progress,
    )
    current = dataset_status(dataset)

    full_export = _output_path(dataset, "full")
    if progress:
        progress({"event": "info", "message": f"Exporting full dataset to {full_export}"})
    export_result = export_dataset(dataset, full_export)
    normalized_export = _output_path(dataset, "domain")
    domain_result = filter_domain_export(full_export, normalized_export, aliases_path=config["aliases"])
    counts = domain_result["counts"]
    targets_met = (counts["nodes"] >= nodes and counts["relations"] >= relations
                   and counts["relation_types"] >= relation_types)
    imported = None
    if targets_met:
        if progress:
            progress({"event": "info", "message": "Normalized targets met; importing entity/relation graph"})
        _load_neo4j_env()
        imported = import_graph(normalized_export)
    return {
        "status": "targets_met" if targets_met else "normalized_targets_not_met",
        "crawl": crawl,
        "collection": collect_result,
        "dataset_status": current,
        "full_export": export_result["output"],
        "normalized_export": domain_result["output"],
        "normalized_counts": counts,
        "targets": {"nodes": nodes, "relations": relations, "relation_types": relation_types},
        "targets_met": targets_met,
        "neo4j": imported,
    }
