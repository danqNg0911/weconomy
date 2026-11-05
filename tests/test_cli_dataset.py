import json
from pathlib import Path

import pytest

from weconomy import cli


def test_collect_dataset_passes_all_options_and_default_config(monkeypatch, tmp_path, capsys):
    captured = {}

    def load_config(path):
        captured["config_path"] = str(path)
        return {"ner_backend": "models"}

    def collect(config, dataset, **kwargs):
        captured.update(config=config, dataset=dataset, **kwargs)
        return {"targets_met": True, "counts": {"articles": 2}}

    monkeypatch.setattr(cli, "load_config", load_config)
    monkeypatch.setattr(cli, "collect_dataset", collect)
    urls = tmp_path / "urls.txt"
    urls.write_text("\ufeffhttps://example.com/a\n\n https://example.com/b \n", encoding="utf-8")

    code = cli.main([
        "collect-dataset", "--dataset", str(tmp_path / "dataset"), "--urls", str(urls),
        "--articles", "2", "--nodes", "3", "--relations", "4", "--relation-types", "5",
        "--max-candidates", "80", "--batch-size", "7", "--resume", "--ner", "gazetteer",
    ])

    assert code == 0
    assert captured["config_path"] == "config/collection.yaml"
    assert captured["urls"] == ["https://example.com/a", "https://example.com/b"]
    assert captured["articles"] == 2
    assert captured["nodes"] == 3
    assert captured["relations"] == 4
    assert captured["relation_types"] == 5
    assert captured["max_candidates"] == 80
    assert captured["batch_size"] == 7
    assert captured["resume"] is True
    assert captured["config"]["ner_backend"] == "gazetteer"
    assert json.loads(capsys.readouterr().out)["targets_met"] is True


def test_collect_dataset_url_input_and_unmet_target_exit_2(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cli, "load_config", lambda path: {})
    captured = {}

    def collect(config, dataset, **kwargs):
        captured.update(kwargs)
        return {"targets_met": False, "reason": "budget_exhausted", "counts": {"articles": 1}}

    monkeypatch.setattr(cli, "collect_dataset", collect)
    urls = tmp_path / "urls.txt"
    urls.write_text("https://one.test/a\n", encoding="utf-8")
    assert cli.main(["--config", "custom.yaml", "collect-dataset", "--urls", str(urls),
                     "--articles", "3"]) == 2
    assert captured["urls"] == ["https://one.test/a"]
    assert captured["resume"] is False
    assert json.loads(capsys.readouterr().out)["reason"] == "budget_exhausted"


def test_collect_dataset_replay_forwards_repeatable_runs(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cli, "load_config", lambda path: {})
    captured = {}
    monkeypatch.setattr(cli, "collect_dataset", lambda config, dataset, **kwargs: (
        captured.update(kwargs) or {"targets_met": True, "counts": {"articles": 1}}))
    first, second = tmp_path / "old-run-a", tmp_path / "old-run-b"
    assert cli.main(["collect-dataset", "--from-run", str(first), "--from-run", str(second),
                     "--dataset", str(tmp_path / "new"), "--max-candidates", "1"]) == 0
    assert captured["from_runs"] == [first, second]
    assert json.loads(capsys.readouterr().out)["counts"]["articles"] == 1


def test_dataset_commands_and_sources_forward_arguments(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cli, "load_config", lambda path: {"sources": "sources.yaml"})
    monkeypatch.setattr(cli, "dataset_status", lambda dataset: {"counts": {"articles": 9}})
    monkeypatch.setattr(cli, "export_dataset", lambda dataset, output: {"output": str(output)})
    captured = {}

    def source_status(config, *, check=False, source_ids=None):
        captured.update(config=config, check=check, source_ids=source_ids)
        return {"sources": [], "checked": check}

    monkeypatch.setattr(cli, "source_status", source_status)
    assert cli.main(["dataset-status", str(tmp_path / "ds")]) == 0
    assert json.loads(capsys.readouterr().out)["counts"]["articles"] == 9
    assert cli.main(["export-dataset", str(tmp_path / "ds"), "--output", str(tmp_path / "out")]) == 0
    assert json.loads(capsys.readouterr().out)["output"] == str(tmp_path / "out")
    assert cli.main(["sources", "--check", "--source", "vnexpress", "--source", "tuoitre"]) == 0
    assert captured == {"config": {"sources": "sources.yaml"}, "check": True,
                       "source_ids": ["vnexpress", "tuoitre"]}
    assert json.loads(capsys.readouterr().out)["checked"] is True


def test_dataset_status_and_export_use_repo_defaults(monkeypatch, capsys):
    captured = {}
    monkeypatch.setattr(cli, "dataset_status", lambda dataset: captured.update(status=dataset) or {})
    monkeypatch.setattr(cli, "export_dataset", lambda dataset, output:
                        captured.update(dataset=dataset, output=output) or {})
    assert cli.main(["dataset-status"]) == 0
    capsys.readouterr()
    assert cli.main(["export-dataset"]) == 0
    capsys.readouterr()
    assert captured == {
        "status": cli._DEFAULT_DATASET,
        "dataset": cli._DEFAULT_DATASET,
        "output": cli._DEFAULT_EXPORT,
    }


def test_dataset_api_errors_exit_1(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cli, "load_config", lambda path: {})

    def fail(*args, **kwargs):
        raise FileNotFoundError("dataset missing")

    monkeypatch.setattr(cli, "collect_dataset", fail)
    urls = tmp_path / "urls.txt"
    urls.write_text("https://example.test/a\n", encoding="utf-8")
    assert cli.main(["collect-dataset", "--urls", str(urls)]) == 1
    assert json.loads(capsys.readouterr().err)["error"] == "FileNotFoundError: dataset missing"


def test_no_target_collection_with_candidate_errors_exits_1(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(cli, "load_config", lambda path: {})
    monkeypatch.setattr(cli, "collect_dataset", lambda *args, **kwargs: {
        "targets_met": False, "reason": "inputs_exhausted", "errors": [{"url": "one"}],
    })
    urls = tmp_path / "urls.txt"
    urls.write_text("https://example.test/a\n", encoding="utf-8")
    assert cli.main(["collect-dataset", "--urls", str(urls)]) == 1
    assert json.loads(capsys.readouterr().out)["errors"]


def test_collect_dataset_requires_explicit_candidate_input(capsys):
    with pytest.raises(SystemExit):
        cli.main(["collect-dataset"])


def test_collect_dataset_uses_repo_default_when_path_is_omitted(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli, "load_config", lambda path: {})
    captured = {}
    monkeypatch.setattr(cli, "collect_dataset", lambda config, dataset, **kwargs:
                        captured.update(dataset=dataset, **kwargs) or {"targets_met": True})
    urls = tmp_path / "urls.txt"
    urls.write_text("https://example.test/story\n", encoding="utf-8")
    assert cli.main(["collect-dataset", "--urls", str(urls)]) == 0
    capsys.readouterr()
    assert captured["dataset"] == cli._DEFAULT_DATASET


def test_collect_crawls_then_replays_runs_into_default_dataset(monkeypatch, capsys):
    captured = {}
    runs = ["data/runs/run-a", "data/runs/run-b"]
    monkeypatch.setattr(cli, "run_collection", lambda config, target_ids=None: {
        "status": "partial", "targets": [{"run_ids": runs}], "errors": [],
    })
    monkeypatch.setattr(cli, "load_config", lambda path: {"loaded_from": str(path)})

    def collect_dataset(config, dataset, **kwargs):
        captured.update(config=config, dataset=dataset, **kwargs)
        return {"targets_met": False, "errors": [], "counts": {"relations": 2}}

    monkeypatch.setattr(cli, "collect_dataset", collect_dataset)
    assert cli.main(["collect"]) == 2
    result = json.loads(capsys.readouterr().out)
    assert captured["from_runs"] == [Path(run) for run in runs]
    assert captured["dataset"] == cli._DEFAULT_DATASET
    assert captured["nodes"] == 1000
    assert captured["relations"] == 5000
    assert captured["relation_types"] == 10
    assert result["status"] == "partial"


def test_existing_schema_command_is_unchanged(capsys):
    assert cli.main(["schema"]) == 0
    assert "tables" in json.loads(capsys.readouterr().out)
