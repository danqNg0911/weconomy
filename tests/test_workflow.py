
import pytest

from weconomy.workflow import graph_cycle


@pytest.fixture(autouse=True)
def isolate_catalog_io(monkeypatch):
    monkeypatch.setattr("weconomy.workflow.register_normalized_export", lambda *_: None)
    monkeypatch.setattr("weconomy.workflow.dataset_seen_urls", lambda _: {"https://example.test/old"})


def test_graph_cycle_normalizes_and_skips_publish_when_targets_are_short(tmp_path, monkeypatch):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "catalog.sqlite3").touch()
    statuses = iter([
        {"counts": {"articles": 3}, "attempts_allocated": 20},
        {"counts": {"articles": 4}, "attempts_allocated": 21},
    ])
    captured = {}
    monkeypatch.setattr("weconomy.workflow._output_path", lambda _dataset, kind: tmp_path / kind)
    monkeypatch.setattr("weconomy.workflow.load_config", lambda _: {"max_articles": 50, "aliases": "aliases.yaml"})
    monkeypatch.setattr("weconomy.workflow.validate_dataset_resume", lambda *_, **__: None)
    monkeypatch.setattr("weconomy.workflow.dataset_status", lambda _: next(statuses))
    monkeypatch.setattr("weconomy.workflow.run_collection", lambda *_args, **_kwargs: {
        "targets": [{"article_urls": ["https://example.test/old", "https://example.test/new"]}], "status": "completed"})

    def collect_dataset(_config, _dataset, **kwargs):
        captured.update(kwargs)
        return {"errors": []}

    monkeypatch.setattr("weconomy.workflow.collect_dataset", collect_dataset)
    monkeypatch.setattr("weconomy.workflow.export_dataset", lambda *_: {"counts": {}})
    monkeypatch.setattr("weconomy.workflow.filter_domain_export", lambda *_args, **_kwargs: {
        "output": "normalized", "counts": {"nodes": 10, "relations": 8, "relation_types": 3}})
    monkeypatch.setattr("weconomy.workflow.import_graph", lambda *_: (_ for _ in ()).throw(AssertionError()))

    result = graph_cycle(dataset, nodes=100, relations=50, relation_types=5, max_candidates=100, max_rounds=1)

    assert captured["resume"] is True
    assert captured["articles"] == 4
    assert captured["max_candidates"] == 21
    assert captured["urls"] == ["https://example.test/new"]
    assert "from_runs" not in captured
    assert result["normalized_export"] == "normalized"
    assert result["full_export"] == str(tmp_path / "full")
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


def test_graph_cycle_reuses_source_analysis_before_collecting_new_urls(tmp_path, monkeypatch):
    dataset = tmp_path / "new-dataset"
    events = []
    statuses = iter([
        {"counts": {"articles": 3}, "attempts_allocated": 20},
        {"counts": {"articles": 4}, "attempts_allocated": 21},
    ])
    monkeypatch.setattr("weconomy.workflow._output_path", lambda _dataset, kind: tmp_path / kind)
    monkeypatch.setattr("weconomy.workflow.load_config", lambda _: {"max_articles": 50, "aliases": "aliases.yaml"})
    monkeypatch.setattr("weconomy.workflow.seed_dataset", lambda source, target: events.append(("seed", source)))
    monkeypatch.setattr("weconomy.workflow.validate_dataset_resume", lambda *_, **__: None)
    monkeypatch.setattr("weconomy.workflow.dataset_status", lambda _: next(statuses))
    monkeypatch.setattr("weconomy.workflow.collect_dataset",
                        lambda _config, _dataset, **kwargs: events.append(("new_articles", kwargs)) or {})
    monkeypatch.setattr("weconomy.workflow.export_dataset", lambda *_: {"counts": {}})
    monkeypatch.setattr("weconomy.workflow.filter_domain_export", lambda *_args, **_kwargs: {
        "output": "normalized", "counts": {"nodes": 10, "relations": 8, "relation_types": 3}})

    def crawl(*_args, **_kwargs):
        events.append(("crawl", {}))
        return {"targets": [{"article_urls": ["https://example.test/new"]}], "status": "completed"}

    monkeypatch.setattr("weconomy.workflow.run_collection", crawl)
    graph_cycle(dataset, source_dataset=tmp_path / "source", nodes=100, relations=50,
                relation_types=5, max_candidates=100, max_rounds=1)

    assert events[0] == ("seed", tmp_path / "source")
    assert events[1][0] == "crawl"
    assert events[2][0] == "new_articles"
    assert "from_runs" not in events[2][1]


@pytest.mark.parametrize("publish", [False, True])
def test_cycle_stops_on_normalized_targets_and_publishes_only_explicitly(tmp_path, monkeypatch, publish):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "catalog.sqlite3").touch()
    state = {"counts": {"articles": 3}, "attempts_allocated": 20}
    calls, imports = [], []
    monkeypatch.setattr("weconomy.workflow.load_config", lambda _: {})
    monkeypatch.setattr("weconomy.workflow.validate_dataset_resume", lambda *_, **__: None)
    monkeypatch.setattr("weconomy.workflow.dataset_status", lambda _: state)
    def export(*args, **kwargs):
        met = state["attempts_allocated"] >= 22
        return {"output": "full"}, {"output": "normalized", "counts": {
            "nodes": 100 if met else 10, "relations": 50 if met else 5, "relation_types": 11}}, met
    monkeypatch.setattr("weconomy.workflow._export_domain", export)
    monkeypatch.setattr("weconomy.workflow.run_collection", lambda *a, **k: {
        "targets": [{"article_urls": ["https://example.test/old", "https://example.test/a", "https://example.test/b"]}]})
    def collect(*args, **kwargs):
        calls.append(kwargs)
        state["attempts_allocated"] += len(kwargs["urls"])
        return {}
    monkeypatch.setattr("weconomy.workflow.collect_dataset", collect)
    monkeypatch.setattr("weconomy.workflow._load_neo4j_env", lambda: None)
    monkeypatch.setattr("weconomy.workflow.import_graph", lambda path: imports.append(path) or {})
    result = graph_cycle(dataset, nodes=100, relations=50, relation_types=11,
                         max_candidates=4, max_rounds=2, publish=publish)
    assert len(calls) == 1
    assert calls[0]["urls"] == ["https://example.test/a", "https://example.test/b"]
    assert result["targets_met"] and result["new_attempts"] == 2
    assert imports == (["normalized"] if publish else [])


def test_cycle_stops_when_discovery_only_returns_old_urls(tmp_path, monkeypatch):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "catalog.sqlite3").touch()
    monkeypatch.setattr("weconomy.workflow.load_config", lambda _: {})
    monkeypatch.setattr("weconomy.workflow.validate_dataset_resume", lambda *_, **__: None)
    monkeypatch.setattr("weconomy.workflow.dataset_status", lambda _: {
        "counts": {"articles": 3}, "attempts_allocated": 20})
    monkeypatch.setattr("weconomy.workflow._export_domain", lambda *a, **k: (
        {"output": "full"}, {"output": "normalized", "counts": {"nodes": 0, "relations": 0, "relation_types": 0}}, False))
    monkeypatch.setattr("weconomy.workflow.run_collection", lambda *a, **k: {
        "targets": [{"article_urls": ["https://example.test/old"]}]})
    monkeypatch.setattr("weconomy.workflow.collect_dataset", lambda *a, **k: pytest.fail("must not reanalyze old URLs"))
    result = graph_cycle(dataset)
    assert result["reason"] == "no_new_urls"
    assert result["new_attempts"] == 0
