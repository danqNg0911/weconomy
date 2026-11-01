import json
from pathlib import Path

import pytest

from weconomy.analytics import analyze
from weconomy.pipeline import load_config, process, read_table
from weconomy.quality import annotation_tasks, evaluate, prf, validate

ROOT = Path(__file__).resolve().parents[1]


def config(tmp_path):
    result = load_config(ROOT / "config/pipeline.yaml")
    result["output"] = str(tmp_path / "runs")
    result["allow_excerpts"] = True
    return result


def test_real_excerpts_end_to_end_and_immutable_runs(tmp_path):
    first, report = process(config(tmp_path), manifest=ROOT / "samples/excerpts/manifest.json")
    second, report2 = process(config(tmp_path), manifest=ROOT / "samples/excerpts/manifest.json")
    assert first != second
    assert report["counts"] == report2["counts"]
    assert report["errors"] == []
    assert report["counts"]["bronze"] == 4
    assert report["counts"]["relations"] > 0
    assert validate(first)["valid"]
    assert read_table(first, "relations") == read_table(second, "relations")
    with pytest.raises(ValueError, match="No accepted full-text"):
        process(config(tmp_path), from_runs=[first, second])
    analytics = analyze(first, small_world=True)
    assert analytics["nodes"] == report["counts"]["entities"]
    assert analytics["small_world_sigma"] is None
    tasks = tmp_path / "tasks.json"
    annotation_tasks(first, tasks)
    with pytest.raises(ValueError, match="reviewer"):
        evaluate(first, tasks)


def test_document_dedup_keeps_bronze_but_not_extra_edges(tmp_path):
    original = ROOT / "samples/excerpts/manifest.json"
    docs = json.loads(original.read_text(encoding="utf-8"))["documents"]
    first = docs[3].copy()
    content = (original.parent / first["path"]).read_bytes()
    (tmp_path / "one.html").write_bytes(content)
    first["path"] = "one.html"
    second = dict(first, url="https://en.wikinews.org/wiki/Duplicate_fixture")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"documents": [first, second]}), encoding="utf-8")
    run, report = process(config(tmp_path), manifest=manifest)
    assert report["duplicate_documents"] == 1
    assert report["counts"]["bronze"] == 2
    assert report["counts"]["relations"] == 1
    assert validate(run)["valid"]


def test_bad_checksum_logged_and_empty_parquet_is_typed(tmp_path):
    row = json.loads((ROOT / "samples/excerpts/manifest.json").read_text(encoding="utf-8"))["documents"][0]
    row["path"] = "bad.html"
    (tmp_path / "bad.html").write_text("corrupt", encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"documents": [row]}), encoding="utf-8")
    run, report = process(config(tmp_path), manifest=manifest)
    assert report["errors"] and report["status"] == "partial"
    assert read_table(run, "relations") == []
    assert validate(run)["valid"]


def test_precision_recall_counts_false_negatives(tmp_path):
    run, _ = process(config(tmp_path), manifest=ROOT / "samples/excerpts/manifest.json")
    path = tmp_path / "labels.json"
    annotation_tasks(run, path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    for task in payload["tasks"]:
        task.update(complete=True, reviewer="unit-test", relations=[], entities=[])
    # Deliberately wrong complete labels: all predicted edges must become false positives.
    path.write_text(json.dumps(payload), encoding="utf-8")
    measured = evaluate(run, path)
    assert measured["relation"]["fp"] > 0
    assert measured["relation"]["precision"] == 0
    assert prf(1, 1, 2)["recall"] == pytest.approx(1/3)
    assert prf(0, 0, 0)["precision"] is None
