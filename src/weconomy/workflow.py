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


def _committed_runs(dataset):
    catalog = Path(dataset) / "catalog.sqlite3"
    if not catalog.is_file():
        return []
    uri = catalog.resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as conn:
        return [Path(row[0]) for row in conn.execute(
            "SELECT run FROM batches WHERE status='committed' AND run IS NOT NULL ORDER BY created_at")
                if Path(row[0]).is_dir()]


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


def _export_domain(dataset, config, *, nodes, relations, relation_types, progress):
    full_export = _output_path(dataset, "full")
    if progress:
        progress({"event": "info", "message": f"Exporting full dataset to {full_export}"})
    export_result = {**export_dataset(dataset, full_export), "output": str(full_export)}
    normalized_export = _output_path(dataset, "domain")
    domain_result = filter_domain_export(full_export, normalized_export, aliases_path=config["aliases"])
    counts = domain_result["counts"]
    targets_met = (counts["nodes"] >= nodes and counts["relations"] >= relations
                   and counts["relation_types"] >= relation_types)
    return export_result, domain_result, targets_met


def graph_cycle(dataset, *, config_path=Path("config/collection.yaml"), target_ids=None,
                source_dataset=Path("data/datasets/international-business-gliner-v1"),
                nodes=2000, relations=5000, relation_types=11, max_candidates=10000,
                batch_size=20, progress=None):
    """Reanalyze saved runs, supplement from configured sources, then publish if targets are met."""
    if any(value <= 0 for value in (nodes, relations, relation_types, max_candidates, batch_size)):
        raise ValueError("Targets, candidate budget, and batch size must be positive")
    dataset = Path(dataset)
    is_new = not (dataset / "catalog.sqlite3").is_file()
    config = load_config(config_path)
    if not is_new:
        validate_dataset_resume(config, dataset)

    collect_result = None
    if is_new:
        old_runs = _committed_runs(source_dataset)
        if not old_runs:
            raise FileNotFoundError(f"No committed source runs found in {source_dataset}")
        if progress:
            progress({"event": "info", "message": f"Reanalyzing {len(old_runs)} saved runs from {source_dataset}"})
        collect_result = collect_dataset(
            config, dataset, from_runs=old_runs, articles=int(config["max_articles"]),
            max_candidates=max_candidates, batch_size=batch_size, progress=progress,
        )

    current = dataset_status(dataset)
    export_result, domain_result, targets_met = _export_domain(
        dataset, config, nodes=nodes, relations=relations, relation_types=relation_types, progress=progress)
    if targets_met:
        _load_neo4j_env()
        imported = import_graph(domain_result["output"])
        return {
            "status": "targets_met", "crawl": None, "collection": collect_result,
            "dataset_status": current, "full_export": export_result["output"],
            "normalized_export": domain_result["output"], "normalized_counts": domain_result["counts"],
            "targets": {"nodes": nodes, "relations": relations, "relation_types": relation_types},
            "targets_met": True, "neo4j": imported,
        }

    if progress:
        progress({"event": "info", "message": "Domain targets are short; crawling configured targets for more articles"})
    crawl = run_collection(config_path, target_ids=target_ids, objectives={},
                           discover_only=True, progress=progress)
    urls = list(dict.fromkeys(url for target in crawl.get("targets", [])
                              for url in target.get("article_urls", [])))
    article_target = current["counts"]["articles"] + int(config["max_articles"])
    candidate_budget = current["attempts_allocated"] + max_candidates
    collect_result = collect_dataset(
        config, dataset, urls=urls,
        articles=article_target,
        max_candidates=candidate_budget, batch_size=batch_size, resume=True, progress=progress,
    )
    current = dataset_status(dataset)
    export_result, domain_result, targets_met = _export_domain(
        dataset, config, nodes=nodes, relations=relations, relation_types=relation_types, progress=progress)
    imported = None
    if targets_met:
        if progress:
            progress({"event": "info", "message": "Normalized targets met; importing entity/relation graph"})
        _load_neo4j_env()
        imported = import_graph(domain_result["output"])
    return {
        "status": "targets_met" if targets_met else "normalized_targets_not_met",
        "crawl": crawl,
        "collection": collect_result,
        "dataset_status": current,
        "full_export": export_result["output"],
        "normalized_export": domain_result["output"],
        "normalized_counts": domain_result["counts"],
        "targets": {"nodes": nodes, "relations": relations, "relation_types": relation_types},
        "targets_met": targets_met,
        "neo4j": imported,
    }
