"""Synthetic HTTP tests; fixtures are excluded from the real article corpus."""
import json
from pathlib import Path

import httpx
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import yaml

from weconomy.access import Access
from weconomy.pipeline import load_config, process, read_table
from weconomy.quality import validate
from weconomy.schema import SCHEMAS

ROOT = Path(__file__).resolve().parents[1]


def test_excerpts_are_quarantined_by_default_and_raw_files_preserved(tmp_path):
    config = load_config(ROOT / "config/pipeline.yaml")
    config["output"] = str(tmp_path / "runs")
    run, report = process(config, manifest=ROOT / "samples/excerpts/manifest.json")
    assert report["quarantined_documents"] == 4
    assert report["content_statuses"] == {"excerpt": 4}
    assert report["counts"]["sentences"] == 0
    assert report["counts"]["entities"] == 0
    assert len(list((run / "bronze/html").glob("*.html"))) == 4
    assert validate(run)["valid"]


def test_collection_gate_and_offline_reprocessing(tmp_path, monkeypatch):
    config = load_config(ROOT / "config/pipeline.yaml")
    config["output"] = str(tmp_path / "runs")
    source_path = tmp_path / "sources.yaml"
    source_path.write_text(yaml.safe_dump({"sources": {"fixture": {
        "hosts": ["example.org"], "allowed": True, "permission_basis": "Unit test fixture",
        "language": "en", "kind": "news", "license": "fixture", "min_interval_seconds": 0,
        "feeds": ["https://example.org/feed"], "body_xpath": "//article",
    }}}), encoding="utf-8")
    config["sources"] = str(source_path)
    calls = []

    def handler(request):
        calls.append(request.url.path)
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        if request.url.path == "/feed":
            return httpx.Response(200, text='''<rss version="2.0"><channel>
                <item><link>https://example.org/full</link></item>
                <item><link>https://example.org/preview</link></item></channel></rss>''')
        if request.url.path == "/alias":
            return httpx.Response(302, headers={"location": "/full"})
        words = " ".join(f"body{i}" for i in range(150))
        tail = "<p>Microsoft acquired GitHub.</p>" if request.url.path in {"/full", "/full2"} else (
            "<p>Subscribe to continue reading the full article.</p>")
        return httpx.Response(200, text=f"<html><head><title>Fixture</title></head>"
                              f"<body><article><h1>Fixture</h1><p>{words}</p>{tail}</article></body></html>",
                              headers={"content-type": "text/html"})

    def make_access(settings):
        client = Access(settings)
        client.client.close()
        client.client = httpx.Client(transport=httpx.MockTransport(handler))
        return client

    monkeypatch.setattr("weconomy.pipeline.Access", make_access)
    monkeypatch.setattr("weconomy.access.socket.getaddrinfo", lambda *a, **k: [(2, 1, 6, "", ("8.8.8.8", 443))])
    run, report = process(config, sources=["fixture"], limit_per_source=2)
    assert report["content_statuses"] == {"body_checked": 1, "partial": 1}
    assert report["counts"]["bronze"] == 2 and report["counts"]["relations"] == 1
    assert report["nlp_documents"] == 1 and report["quarantined_documents"] == 1
    assert validate(run)["valid"]
    full_doc = next(a["document_id"] for a in read_table(run, "articles") if a["nlp_eligible"])
    assert {m["document_id"] for m in read_table(run, "mentions")} == {full_doc}
    call_count = len(calls)
    replay, replay_report = process(config, from_run=run)
    assert len(calls) == call_count
    assert replay_report["counts"] == report["counts"]
    assert read_table(replay, "relations") == read_table(run, "relations")
    assert validate(replay)["valid"]
    # Merging replays is not additional news; quarantined previews must stay out of the corpus.
    merged, merged_report = process(config, from_runs=[run, replay])
    assert len(calls) == call_count
    assert merged_report["counts"]["articles"] == 1
    assert merged_report["counts"]["relations"] == 1
    assert merged_report["content_statuses"] == {"body_checked": 1}
    assert validate(merged)["valid"]
    duplicate_run, _ = process(config, urls=["https://example.org/full2"])
    deduplicated, dedup_report = process(config, from_runs=[merged, duplicate_run])
    assert dedup_report["counts"]["articles"] == 2
    assert dedup_report["duplicate_documents"] == 1
    assert dedup_report["counts"]["relations"] == 1
    assert validate(deduplicated)["valid"]
    full_requests = calls.count("/full")
    resumed, resumed_report = process(config, sources=["fixture"], limit_per_source=2, skip_runs=[merged])
    assert calls.count("/full") == full_requests
    assert resumed_report["known_fulltext_urls"] == 1
    assert resumed_report["counts"]["articles"] == 1  # Failed preview may be tried again.
    assert validate(resumed)["valid"]
    monkeypatch.setattr(Access, "discover_records", lambda *args, **kwargs: [])
    unchanged, unchanged_report = process(config, sources=["fixture"], skip_runs=[merged])
    assert unchanged_report["status"] == "no_new_documents"
    assert unchanged_report["counts"]["articles"] == 0
    assert unchanged_report["errors"] == []
    assert validate(unchanged)["valid"]
    redirected, redirected_report = process(config, urls=["https://example.org/alias", "https://example.org/full"])
    assert redirected_report["counts"]["bronze"] == 1
    assert redirected_report["counts"]["relations"] == 1
    assert validate(redirected)["valid"]
    # Validation must catch accidental bypass of the content gate.
    articles = read_table(run, "articles")
    articles[0]["nlp_eligible"] = False
    pq.write_table(pa.Table.from_pylist(articles, schema=SCHEMAS["articles"]), run / "silver/articles.parquet")
    assert not validate(run)["valid"]


def test_nlp_failure_does_not_publish_half_a_document(tmp_path, monkeypatch):
    config = load_config(ROOT / "config/pipeline.yaml")
    config.update(output=str(tmp_path / "runs"), allow_excerpts=True)
    original = json.loads((ROOT / "samples/excerpts/manifest.json").read_text("utf-8"))
    row = original["documents"][3]
    (tmp_path / row["path"]).write_bytes((ROOT / "samples/excerpts" / row["path"]).read_bytes())
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"documents": [row]}), encoding="utf-8")
    from weconomy.nlp import NLP
    original_mentions = NLP.mentions
    calls = 0

    def fail_after_first(self, text, language):
        nonlocal calls
        calls += 1
        if calls > 1:
            raise ValueError("Simulated token alignment failure")
        return original_mentions(self, text, language)

    monkeypatch.setattr(NLP, "mentions", fail_after_first)
    run, report = process(config, manifest=manifest)
    assert report["errors"]
    assert report["counts"]["sentences"] == report["counts"]["entities"] == report["counts"]["relations"] == 0
    assert not read_table(run, "articles")[0]["nlp_eligible"]
    assert validate(run)["valid"]


@pytest.mark.parametrize("case", ["missing_manifest", "invalid_json", "oversize_manifest", "two_inputs",
                                  "missing_run", "empty_sources", "source_budget", "empty_merge",
                                  "skip_without_sources"])
def test_invalid_input_does_not_create_run_directory(tmp_path, case):
    config = load_config(ROOT / "config/pipeline.yaml")
    config["output"] = str(tmp_path / "runs")
    path = tmp_path / "manifest.json"
    if case == "missing_manifest":
        args = {"manifest": path}
    elif case == "invalid_json":
        path.write_text("{broken", encoding="utf-8")
        args = {"manifest": path}
    elif case == "oversize_manifest":
        config["max_documents"] = 1
        path.write_text(json.dumps({"documents": [{}, {}]}), encoding="utf-8")
        args = {"manifest": path}
    elif case == "two_inputs":
        args = {"manifest": path, "urls": []}
    elif case == "missing_run":
        args = {"from_run": tmp_path / "missing"}
    elif case == "empty_sources":
        args = {"sources": []}
    elif case == "empty_merge":
        args = {"from_runs": []}
    elif case == "skip_without_sources":
        args = {"urls": [], "skip_runs": [tmp_path / "missing"]}
    else:
        config["max_documents"] = 1
        args = {"sources": ["vnexpress"], "limit_per_source": 2}
    with pytest.raises((ValueError, FileNotFoundError)):
        process(config, **args)
    assert not Path(config["output"]).exists()
