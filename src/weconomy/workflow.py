"""Bounded collection, domain normalization, and graph publication cycle."""
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .crawler import run_collection
from .dataset import (
    collect_dataset,
    dataset_seen_urls,
    dataset_status,
    export_dataset,
    register_normalized_export,
    seed_dataset,
    validate_dataset_resume,
)
from .domain_filter import filter_domain_export
from .graph import import_graph
from .pipeline import load_config


def _output_path(dataset, kind):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    layer = Path("data/normalized") if kind == "domain" else Path("data/analysis/exports")
    return layer / f"{Path(dataset).name}-{kind}-{stamp}-{uuid4().hex[:6]}"


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
    domain_result = filter_domain_export(
        full_export, normalized_export, aliases_path=config["aliases"],
        targets={"nodes": nodes, "relations": relations, "relation_types": relation_types})
    register_normalized_export(dataset, domain_result["output"])
    counts = domain_result["counts"]
    targets_met = (counts["nodes"] >= nodes and counts["relations"] >= relations
                   and counts["relation_types"] >= relation_types)
    return export_result, domain_result, targets_met


def graph_cycle(dataset, *, config_path=Path("config/collection.yaml"), target_ids=None,
                source_dataset=Path("data/datasets/international-business-gliner-v2"),
                nodes=2000, relations=5000, relation_types=11, max_candidates=10000,
                batch_size=20, progress=None, max_rounds=3, allow_processing_upgrade=False,
                publish=False):
    """Verify existing analysis, then collect new URLs within explicit candidate/round budgets."""
    if any(value <= 0 for value in (nodes, relations, relation_types, max_candidates, batch_size, max_rounds)):
        raise ValueError("Targets, candidate budget, and batch size must be positive")
    dataset = Path(dataset)
    is_new = not (dataset / "catalog.sqlite3").is_file()
    config = load_config(config_path)
    if is_new:
        seed_dataset(source_dataset, dataset)
        if progress:
            progress({"event": "info", "message": f"Reused committed analysis from {source_dataset}; no old NLP replay"})
    current = dataset_status(dataset)
    export_result, domain_result, targets_met = _export_domain(
        dataset, config, nodes=nodes, relations=relations, relation_types=relation_types, progress=progress)
    rounds, crawl, collect_result = [], None, None
    initial_attempts = current["attempts_allocated"]
    reason = "targets_met" if targets_met else "round_limit"
    if not targets_met:
        validate_dataset_resume(config, dataset, allow_processing_upgrade=allow_processing_upgrade)
    per_round = max(1, (max_candidates + max_rounds - 1) // max_rounds)
    for number in range(1, max_rounds + 1):
        if targets_met:
            reason = "targets_met"
            break
        remaining = max_candidates - (current["attempts_allocated"] - initial_attempts)
        if remaining <= 0:
            reason = "candidate_budget_exhausted"
            break
        seen = dataset_seen_urls(dataset)
        if progress:
            progress({"event": "info", "message": f"Domain targets short; discovering NEW articles, round {number}/{max_rounds}"})
        crawl = run_collection(config_path, target_ids=target_ids, objectives={},
                               discover_only=True, progress=progress, exclude_urls=seen,
                               max_new_urls=min(remaining, per_round))
        urls = list(dict.fromkeys(url for target in crawl.get("targets", [])
                                  for url in target.get("article_urls", []) if url not in seen))
        urls = urls[:min(remaining, per_round)]
        if not urls:
            reason = "discovery_failed" if crawl.get("errors") else "no_new_urls"
            break
        before = current["attempts_allocated"]
        collect_result = collect_dataset(
            config, dataset, urls=urls, articles=current["counts"]["articles"] + len(urls),
            max_candidates=before + len(urls), batch_size=batch_size, resume=True, progress=progress,
            allow_processing_upgrade=allow_processing_upgrade)
        current = dataset_status(dataset)
        export_result, domain_result, targets_met = _export_domain(
            dataset, config, nodes=nodes, relations=relations, relation_types=relation_types, progress=progress)
        rounds.append({"round": number, "new_urls": len(urls), "counts": domain_result["counts"],
                       "normalized_export": domain_result["output"]})
        if current["attempts_allocated"] <= before:
            reason = "no_collection_progress"
            break
    if targets_met:
        reason = "targets_met"
    elif current["attempts_allocated"] - initial_attempts >= max_candidates:
        reason = "candidate_budget_exhausted"
    imported = None
    if targets_met and publish:
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
        "reason": reason, "rounds": rounds,
        "new_attempts": current["attempts_allocated"] - initial_attempts,
        "remaining": {key: max(0, value - domain_result["counts"][key]) for key, value in
                      {"nodes": nodes, "relations": relations, "relation_types": relation_types}.items()},
    }
