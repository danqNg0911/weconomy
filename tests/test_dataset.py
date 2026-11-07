"""Offline tests for the dataset API. All source content here is TEST_ONLY."""
import json
from pathlib import Path

import pytest
import yaml

from weconomy import dataset, pipeline
from weconomy.pipeline import load_config

ROOT = Path(__file__).resolve().parents[1]
EDGE = "Microsoft acquired GitHub."


def _story(tail=EDGE, prefix="syntheticword"):
    lead = " ".join(f"{prefix}{i}" for i in range(150))
    return f"<html><head><title>TEST_ONLY fixture</title></head><body><article><p>{lead}</p><p>TEST_ONLY startup company report.</p><p>{tail}</p></article></body></html>"


class FixtureAccess:
    """Finite synthetic discovery records; this never makes a network request."""

    def __init__(self, records):
        self.records = records

    def policy(self, url):
        return "fixture", {"kind": "news", "allowed": True, "reason": "TEST_ONLY fixture"}

    def close(self):
        pass


@pytest.fixture(autouse=True)
def _dataset_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _setup(tmp_path, monkeypatch, stories):
    """Route dataset discovery through fixtures and processing through real pipeline.process."""
    config = load_config(ROOT / "config/pipeline.yaml")
    config["output"] = str(tmp_path / "runs")
    config["min_article_words"] = 100
    config["min_text_chars"] = 100
    config["allow_excerpts"] = False
    source_file = tmp_path / "sources.yaml"
    source_file.write_text(yaml.safe_dump({"sources": {"fixture": {
        "allowed": True, "permission_basis": "TEST_ONLY", "hosts": ["example.org"],
        "kind": "news",
        "body_xpath": "//article", "min_interval_seconds": 0,
        "language": "en", "license": "TEST_ONLY synthetic fixture",
    }}}), encoding="utf-8")
    config["sources"] = str(source_file)
    config["test_urls"] = list(stories)
    records = [{"url": url} for url in stories]
    monkeypatch.setattr(dataset, "Access", lambda settings: FixtureAccess(records))

    real_process = pipeline.process
    calls = []

    def offline_process(batch_config, *args, **kwargs):
        urls = kwargs.get("urls") or []
        calls.extend(urls)
        fixture_dir = tmp_path / "source-fixture"
        fixture_dir.mkdir(exist_ok=True)
        documents = []
        for i, url in enumerate(urls):
            html_path = fixture_dir / f"{i}.html"
            html_path.write_text(stories[url], encoding="utf-8")
            documents.append({
                "url": url, "source_id": "fixture", "kind": "news",
                "license": "TEST_ONLY synthetic fixture",
                "attribution": "TEST_ONLY; synthetic content, not collected journalism",
                "capture_scope": "full_page", "path": html_path.name,
                "retrieved_at": "2025-01-01T00:00:00Z",
            })
        manifest = fixture_dir / f"manifest-{len(calls)}.json"
        manifest.write_text(json.dumps({"documents": documents}), encoding="utf-8")
        return real_process(batch_config, manifest=manifest,
                            nlp_engine=kwargs.get("nlp_engine"))

    monkeypatch.setattr(pipeline, "process", offline_process)
    return config, calls


def test_zero_targets_still_collects_finite_candidates(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, calls = _setup(tmp_path, monkeypatch, {url: _story()})
    dataset.collect_dataset(config, "zero", urls=config["test_urls"])
    status = dataset.dataset_status("zero")
    assert calls == [url]
    assert status["counts"]["articles"] == 1


def test_targets_are_simultaneous_and_nodes_come_from_real_extraction(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, _ = _setup(tmp_path, monkeypatch, {url: _story()})
    dataset.collect_dataset(config, "targets", urls=config["test_urls"], articles=2, nodes=3, batch_size=1)
    status = dataset.dataset_status("targets")
    assert status["counts"]["articles"] == 1
    assert status["counts"]["nodes"] == 2
    assert not status["targets_met"]


def test_attempt_budget_resume_and_budget_increase(tmp_path, monkeypatch):
    urls = [f"https://example.org/{i}" for i in range(4)]
    config, calls = _setup(tmp_path, monkeypatch, {u: _story() for u in urls})
    dataset.collect_dataset(config, "budget", urls=config["test_urls"], max_candidates=2, batch_size=1)
    assert len(calls) == 2
    dataset.collect_dataset(config, "budget", urls=config["test_urls"], max_candidates=2, batch_size=1, resume=True)
    assert len(calls) == 2
    dataset.collect_dataset(config, "budget", urls=config["test_urls"], max_candidates=4, batch_size=1, resume=True)
    assert len(calls) == 4
    assert dataset.dataset_status("budget")["attempts_allocated"] == 4


def test_nlp_model_is_loaded_once_for_multiple_batches(tmp_path, monkeypatch):
    urls = [f"https://example.org/{i}" for i in range(2)]
    config, _ = _setup(tmp_path, monkeypatch, {u: _story() for u in urls})
    original = dataset.nlp.NLP
    created = []

    def counted(settings):
        created.append(True)
        return original(settings)

    monkeypatch.setattr(dataset.nlp, "NLP", counted)
    dataset.collect_dataset(config, "reuse-nlp", urls=config["test_urls"],
                            max_candidates=2, batch_size=1)
    assert len(created) == 1


def test_duplicates_across_batches_and_same_edge_stories(tmp_path, monkeypatch):
    urls = [f"https://example.org/{i}" for i in range(3)]
    config, _ = _setup(tmp_path, monkeypatch, {
        urls[0]: _story(), urls[1]: _story(),
        urls[2]: _story("A synthetic report says Microsoft acquired GitHub."),
    })
    dataset.collect_dataset(config, "dedupe", urls=config["test_urls"], max_candidates=3, batch_size=1)
    status = dataset.dataset_status("dedupe")
    assert status["counts"]["articles"] == 2
    assert status["counts"]["relations"] == 1
    assert status["counts"]["nodes"] == 2


def test_open_relation_types_are_counted_without_static_type_constraints(tmp_path):
    conn = dataset._connect(tmp_path / "open-relations")
    try:
        dataset._put(conn, "entities", "a", {"entity_id": "a", "entity_type": "ORG"})
        dataset._put(conn, "entities", "b", {"entity_id": "b", "entity_type": "PLACE"})
        dataset._put(conn, "relations", "c", {"subject_id": "a", "predicate": "LICENSES_TECHNOLOGY_TO",
                                                   "object_id": "b"})
        claims, connected = dataset._graph_claims(conn)
        assert len(claims) == 1
        assert connected == {"a", "b"}
    finally:
        conn.close()


def test_relation_types_validation_and_export_is_unique_and_one_shot(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, _ = _setup(tmp_path, monkeypatch, {url: _story()})
    with pytest.raises((TypeError, ValueError)):
        dataset.collect_dataset(config, "bad-type", relation_types=["MADE_UP"])
    with pytest.raises((TypeError, ValueError)):
        dataset.collect_dataset(config, "bad-budget", max_candidates=-1)
    dataset.collect_dataset(config, "export", urls=config["test_urls"])
    output = tmp_path / "export-output"
    result = dataset.export_dataset("export", output)
    assert result["counts"]["nodes"] == 2
    entities = [json.loads(line) for line in (output / "entities.jsonl").read_text().splitlines()]
    claims = [json.loads(line) for line in (output / "claims.jsonl").read_text().splitlines()]
    assert len({row["entity_id"] for row in entities}) == 2
    assert claims and claims[0]["source_run"] and claims[0]["source_id"] == "fixture"
    with pytest.raises((FileExistsError, ValueError)):
        dataset.export_dataset("export", output)


def test_resume_requires_existing_catalog_and_compatible_config(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, _ = _setup(tmp_path, monkeypatch, {url: _story()})
    with pytest.raises((FileNotFoundError, ValueError)):
        dataset.collect_dataset(config, "missing", resume=True)
    dataset.collect_dataset(config, "existing", urls=config["test_urls"])
    dataset.validate_dataset_resume(config, "existing")
    collection_changed = dict(config, targets=[{"id": "another-category"}],
                              crawl={"max_pages_per_target": 2}, batch_size=5, max_articles=10)
    dataset.validate_dataset_resume(collection_changed, "existing")
    changed = dict(config, min_article_words=101)
    with pytest.raises(ValueError, match="fingerprint"):
        dataset.validate_dataset_resume(changed, "existing")
    with pytest.raises(ValueError):
        dataset.collect_dataset(changed, "existing", urls=config["test_urls"], resume=True)


def test_status_and_export_do_not_initialize_nlp(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, _ = _setup(tmp_path, monkeypatch, {url: _story()})
    dataset.collect_dataset(config, "no-nlp", urls=config["test_urls"])
    monkeypatch.setattr("weconomy.nlp.NLP.__init__", lambda *a, **k: (_ for _ in ()).throw(AssertionError("NLP initialized")))
    assert dataset.dataset_status("no-nlp")["counts"]["articles"] == 1
    dataset.export_dataset("no-nlp", tmp_path / "no-nlp-export")


def test_interrupted_commit_recovers_pending_run_without_reprocessing(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, calls = _setup(tmp_path, monkeypatch, {url: _story()})
    ingest = dataset._ingest
    raised = False

    def interrupt_once(*args, **kwargs):
        nonlocal raised
        result = ingest(*args, **kwargs)
        if not raised:
            raised = True
            raise KeyboardInterrupt
        return result

    monkeypatch.setattr(dataset, "_ingest", interrupt_once)
    with pytest.raises(KeyboardInterrupt):
        dataset.collect_dataset(config, "recover", urls=config["test_urls"], batch_size=1)
    monkeypatch.setattr(dataset, "_ingest", ingest)
    dataset.collect_dataset(config, "recover", urls=config["test_urls"], batch_size=1, resume=True)
    assert calls == [url]
    assert dataset.dataset_status("recover")["counts"]["articles"] == 1


def test_batch_error_does_not_stop_later_batches_and_resume_retries_failed_urls(tmp_path, monkeypatch):
    urls = ["https://example.org/first", "https://example.org/second"]
    config, calls = _setup(tmp_path, monkeypatch, {
        urls[0]: _story(prefix="firstword"), urls[1]: _story(prefix="secondword")})
    process = pipeline.process
    failed = set()

    def fail_first_once(*args, **kwargs):
        batch_urls = kwargs.get("urls") or []
        if batch_urls and batch_urls[0] == urls[0] and urls[0] not in failed:
            failed.add(urls[0])
            raise RuntimeError("TEST_ONLY transient failure")
        return process(*args, **kwargs)

    monkeypatch.setattr(pipeline, "process", fail_first_once)
    status = dataset.collect_dataset(config, "retry", urls=urls, batch_size=1, max_candidates=2)
    assert calls == [urls[1]]
    assert status["counts"]["articles"] == 1
    assert status["errors"][0]["error_type"] == "RuntimeError"

    status = dataset.collect_dataset(config, "retry", urls=urls, batch_size=1,
                                     max_candidates=3, resume=True)
    assert calls == [urls[1], urls[0]]
    assert status["counts"]["articles"] == 2
    assert status["errors"] == []
    assert len(status["error_history"]) == 1


def test_snapshot_counts_only_connected_allowed_typed_nodes(tmp_path):
    conn = dataset._connect(tmp_path / "snapshot")
    dataset._put(conn, "entities", "p", {"entity_id": "p", "name": "Person", "entity_type": "PERSON"})
    dataset._put(conn, "entities", "o", {"entity_id": "o", "name": "Org", "entity_type": "ORG"})
    dataset._put(conn, "entities", "i", {"entity_id": "i", "name": "Isolate", "entity_type": "ORG"})
    dataset._put(conn, "entities", "x", {"entity_id": "x", "name": "Other", "entity_type": "LOCATION"})
    dataset._put(conn, "relations", "c1", {"subject_id": "p", "predicate": "CEO_OF", "object_id": "o"})
    dataset._put(conn, "relations", "c2", {"subject_id": "p", "predicate": "CEO_OF", "object_id": "x"})
    assert dataset._snapshot(conn)["nodes"] == 2
    assert dataset._snapshot(conn)["relations"] == 1
    conn.close()


def test_entity_record_id_accepts_display_case_variants(tmp_path):
    conn = dataset._connect(tmp_path / "entities")
    dataset._put(conn, "entities", "same", {"entity_id": "same", "name": "Microsoft", "entity_type": "ORG"})
    dataset._put(conn, "entities", "same", {"entity_id": "same", "name": "MICROSOFT", "entity_type": "ORG"})
    assert dataset._rows(conn, "entities")[0]["name"] == "Microsoft"
    conn.close()


def test_interrupted_batch_without_manifest_is_requeued(tmp_path):
    conn = dataset._connect(tmp_path / "recover-empty")
    batch_root = tmp_path / "recover-empty" / "batches" / "lost"
    batch_root.mkdir(parents=True)
    conn.execute("INSERT INTO batches VALUES(?,?,?,?,?,?)", ("lost", str(batch_root), json.dumps(["https://example.org/lost"]), "pending", None, 1))
    conn.execute("INSERT INTO queue VALUES(?,?,?,?,?,?)", ("https://example.org/lost", "fixture", "pending", None, "lost", 1))
    dataset._recover(conn, tmp_path / "recover-empty")
    row = conn.execute("SELECT status,batch_id FROM queue").fetchone()
    assert tuple(row) == ("queued", None)
    assert conn.execute("SELECT status FROM batches").fetchone()[0] == "interrupted"
    conn.close()


def test_status_is_readable_during_writer_and_does_not_unlock_writer(tmp_path):
    target = tmp_path / "live-status"
    with dataset._writer_lock(target):
        with dataset._connect(target) as conn:
            dataset._set_meta(conn, "reason", "inputs_exhausted")
        assert dataset.dataset_status(target)["counts"]["articles"] == 0
        with pytest.raises(OSError):
            with dataset._writer_lock(target):
                pass


def test_live_status_uses_current_invocation_targets(tmp_path, monkeypatch):
    target = tmp_path / "live-targets"
    conn = dataset._connect(target)
    dataset._put(conn, "articles", "old", {"document_id": "old", "canonical_url": "https://example.org/old"})
    dataset._set_meta(conn, "targets", {"articles": 1, "nodes": None,
                                         "relations": None, "relation_types": None})
    dataset._set_meta(conn, "reason", "targets_met")
    conn.close()
    config = load_config(ROOT / "config/pipeline.yaml")
    config["sources"] = str(target / "sources.yaml")
    Path(config["sources"]).write_text(yaml.safe_dump({"sources": {"fixture": {
        "allowed": True, "permission_basis": "TEST_ONLY", "hosts": ["example.org"],
        "kind": "news",
    }}}), encoding="utf-8")
    config["aliases"] = str(ROOT / "config/entities.yaml")
    observed = []

    class ObservingAccess(FixtureAccess):
        def __init__(self, records):
            observed.append(dataset.dataset_status(target))
            super().__init__(records)

    monkeypatch.setattr(dataset, "Access", lambda settings: ObservingAccess([]))
    dataset.collect_dataset(config, target, urls=[], articles=3, max_candidates=1, resume=True)
    assert observed[0]["reason"] == "running"
    assert observed[0]["targets"]["articles"] == 3
    assert observed[0]["targets_met"] is False


def test_export_preserves_run_lineage_when_there_are_no_claims(tmp_path, monkeypatch):
    url = "https://example.org/no-claim"
    config, _ = _setup(tmp_path, monkeypatch, {url: _story("A routine quarterly report was published.")})
    dataset.collect_dataset(config, "no-claims", urls=config["test_urls"])
    assert dataset.dataset_status("no-claims")["counts"]["claims"] == 0
    manifest = dataset.export_dataset("no-claims", tmp_path / "no-claims-export")
    assert manifest["source_runs"]


def _make_replay_archive(tmp_path, monkeypatch, stories):
    config = load_config(ROOT / "config/pipeline.yaml")
    config.update(output=str(tmp_path / "runs"), ner_backend="gazetteer",
                  min_article_words=100, min_text_chars=100, allow_excerpts=False)
    sources = {
        "fixture": {"allowed": True, "permission_basis": "TEST_ONLY", "hosts": ["example.org"],
                    "kind": "news", "body_xpath": "//article", "language": "en",
                    "license": "TEST_ONLY synthetic fixture"},
        "techcrunch": {"allowed": True, "permission_basis": "TEST_ONLY", "hosts": ["techcrunch.com"],
                       "kind": "news", "body_xpath": "//article", "language": "en",
                       "license": "TEST_ONLY synthetic fixture"},
        "voa": {"allowed": False, "permission_basis": "TEST_ONLY excluded", "hosts": ["voanews.com"],
                "kind": "news", "body_xpath": "//article", "language": "en",
                "license": "TEST_ONLY synthetic fixture"},
    }
    sources_path = tmp_path / "replay-sources.yaml"
    sources_path.write_text(yaml.safe_dump({"sources": sources}), encoding="utf-8")
    config["sources"] = str(sources_path)
    fixture = tmp_path / "replay-fixture"
    fixture.mkdir()
    documents = []
    for index, (url, (source_id, html)) in enumerate(stories.items()):
        path = fixture / f"{index}.html"
        path.write_text(html, encoding="utf-8")
        documents.append({"url": url, "source_id": source_id, "kind": "news",
                          "license": "TEST_ONLY synthetic fixture", "attribution": "TEST_ONLY synthetic",
                          "capture_scope": "full_page", "path": path.name,
                          "retrieved_at": "2025-01-01T00:00:00Z", "language_hint": "en"})
    manifest = fixture / "manifest.json"
    manifest.write_text(json.dumps({"documents": documents}), encoding="utf-8")
    run, report = pipeline.process(config, manifest=manifest, nlp_engine=dataset.nlp.NLP(config))
    assert report["status"] in {"completed", "partial"}
    return config, run


def test_offline_replay_stages_only_currently_allowed_archive_bodies(tmp_path, monkeypatch):
    allowed_url = "https://example.org/one"
    stories = {allowed_url: ("fixture", _story()),
               "https://techcrunch.com/two": ("techcrunch", _story("TEST_ONLY news.", "techword")),
               "https://voanews.com/three": ("voa", _story("TEST_ONLY news."))}
    config, archive = _make_replay_archive(tmp_path, monkeypatch, stories)
    monkeypatch.setattr("weconomy.access.Access.fetch",
                        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network fetch called")))
    target = tmp_path / "replayed"
    result = dataset.collect_dataset(config, target, from_runs=[archive], max_candidates=4, batch_size=1)
    assert result["attempts_allocated"] == 2
    assert result["counts"]["articles"] == 2
    with dataset.closing(dataset._read_connect(target)) as conn:
        article = dataset._rows(conn, "articles")[0]
        bronze = dataset._rows(conn, "bronze")[0]
    assert article["archive_source_run"] == str(archive)
    assert article["archive_source_document_id"] == article["document_id"]
    assert bronze["archive_raw_sha256"] == bronze["raw_sha256"]
    assert "license" not in bronze


def test_replay_resume_is_deduplicated_and_rejects_changed_source_archive(tmp_path, monkeypatch):
    url = "https://example.org/one"
    config, archive = _make_replay_archive(tmp_path, monkeypatch, {url: ("fixture", _story())})
    target = tmp_path / "replay-resume"
    first = dataset.collect_dataset(config, target, from_runs=[archive], max_candidates=2, batch_size=1)
    second = dataset.collect_dataset(config, target, from_runs=[archive], max_candidates=2,
                                     batch_size=1, resume=True)
    assert first["counts"]["articles"] == second["counts"]["articles"] == 1
    assert second["attempts_allocated"] == first["attempts_allocated"]
    bronze_file = archive / "bronze" / "bronze.parquet"
    with pytest.raises(ValueError, match="checksum mismatch"):
        table = pipeline.pq.read_table(bronze_file)
        rows = table.to_pylist()
        rows[0]["raw_bytes"] += b"modified"
        pipeline.pq.write_table(pipeline.pa.Table.from_pylist(rows, schema=dataset.schema.SCHEMAS["bronze"]),
                                bronze_file)
        dataset.collect_dataset(config, target, from_runs=[archive], max_candidates=2,
                                batch_size=1, resume=True)
