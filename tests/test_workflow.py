from pathlib import Path

import pytest

from weconomy.workflow import graph_cycle


def test_graph_cycle_normalizes_and_skips_publish_when_targets_are_short(tmp_path, monkeypatch):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "catalog.sqlite3").touch()
    statuses = iter([
        {"counts": {"articles": 3}, "attempts_allocated": 20},
        {"counts": {"articles": 4}, "attempts_allocated": 21},
    ])
    captured = {}
    monkeypatch.setattr("weconomy.workflow.load_config", lambda _: {"max_articles": 50, "aliases": "aliases.yaml"})
    monkeypatch.setattr("weconomy.workflow.validate_dataset_resume", lambda *_: None)
    monkeypatch.setattr("weconomy.workflow.dataset_status", lambda _: next(statuses))
    monkeypatch.setattr("weconomy.workflow._replay_runs", lambda _: [Path("old-run")])
    monkeypatch.setattr("weconomy.workflow.run_collection", lambda *_args, **_kwargs: {
        "targets": [{"run_ids": ["new-run"]}], "status": "completed"})

    def collect_dataset(_config, _dataset, **kwargs):
        captured.update(kwargs)
        return {"errors": []}

    monkeypatch.setattr("weconomy.workflow.collect_dataset", collect_dataset)
    monkeypatch.setattr("weconomy.workflow.export_dataset", lambda *_: {"output": "full"})
    monkeypatch.setattr("weconomy.workflow.filter_domain_export", lambda *_args, **_kwargs: {
        "output": "normalized", "counts": {"nodes": 10, "relations": 8, "relation_types": 3}})
    monkeypatch.setattr("weconomy.workflow.import_graph", lambda *_: (_ for _ in ()).throw(AssertionError()))

    result = graph_cycle(dataset, nodes=100, relations=50, relation_types=5, max_candidates=100)

    assert captured["resume"] is True
    assert captured["articles"] == 53
    assert captured["max_candidates"] == 120
    assert captured["from_runs"] == [Path("old-run"), Path("new-run")]
    assert result["normalized_export"] == "normalized"
    assert result["status"] == "normalized_targets_not_met"
    assert result["neo4j"] is None


def test_graph_cycle_rejects_invalid_limits_before_crawling(tmp_path, monkeypatch):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "catalog.sqlite3").touch()
    monkeypatch.setattr("weconomy.workflow.load_config", lambda _: {})
    monkeypatch.setattr("weconomy.workflow.validate_dataset_resume", lambda *_: None)
    monkeypatch.setattr("weconomy.workflow.dataset_status", lambda _: {"counts": {}, "attempts_allocated": 0})
    monkeypatch.setattr("weconomy.workflow.run_collection",
                        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("must not crawl")))

    with pytest.raises(ValueError, match="must be positive"):
        graph_cycle(dataset, max_candidates=0)
