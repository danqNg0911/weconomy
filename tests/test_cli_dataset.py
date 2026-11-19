import json
from io import StringIO

import pytest

from weconomy import cli


def test_console_progress_shows_fulltext_counts(capsys):
    cli._console_progress({"event": "article_done", "stage": "crawl", "index": 1,
                           "total": 1, "status": "body_checked", "title": "Bài test",
                           "word_count": 1200, "body_paragraphs": 18, "nlp_sentences": 44,
                           "entities": 5, "relations": 2})
    output = capsys.readouterr().err
    assert "1200 từ, 18 đoạn, 44 câu NLP" in output


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
    monkeypatch.setattr(cli, "validate_dataset_resume", lambda config, dataset, **kwargs: None)
    (tmp_path / "dataset").mkdir()
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


def test_force_uses_new_dataset_path_and_preserves_existing(monkeypatch, tmp_path, capsys):
    existing = tmp_path / "dataset"
    existing.mkdir()
    urls = tmp_path / "urls.txt"
    urls.write_text("https://example.com/a\n", encoding="utf-8")
    captured = {}
    monkeypatch.setattr(cli, "load_config", lambda path: {})
    monkeypatch.setattr(cli, "collect_dataset", lambda config, dataset, **kwargs: (
        captured.update(dataset=dataset, **kwargs) or {"targets_met": True, "counts": {"articles": 1}}))

    assert cli.main(["collect-dataset", "--dataset", str(existing), "--force", "--urls", str(urls)]) == 0
    assert captured["dataset"] != existing
    assert captured["dataset"].parent == existing.parent
    assert existing.is_dir()
    assert not captured["dataset"].exists()
    capsys.readouterr()


def test_existing_dataset_fails_before_collect_crawls(monkeypatch, tmp_path, capsys):
    existing = tmp_path / "dataset"
    existing.mkdir()
    monkeypatch.setattr(cli, "run_collection", lambda *a, **k: pytest.fail("crawl must not start"))

    assert cli.main(["collect", "--dataset", str(existing)]) == 1
    error = capsys.readouterr().err
    assert "Dataset đã tồn tại" in error
    assert "--resume hoặc --force" in error


def test_incompatible_resume_fails_before_collect_crawls(monkeypatch, tmp_path, capsys):
    existing = tmp_path / "dataset"
    existing.mkdir()
    monkeypatch.setattr(cli, "load_config", lambda path: {})
    monkeypatch.setattr(cli, "validate_dataset_resume",
                        lambda config, dataset, **kwargs: (_ for _ in ()).throw(ValueError("fingerprint mismatch")))
    monkeypatch.setattr(cli, "run_collection", lambda *a, **k: pytest.fail("crawl must not start"))

    assert cli.main(["collect", "--dataset", str(existing), "--resume"]) == 1
    assert "fingerprint mismatch" in capsys.readouterr().err


def test_progress_messages_use_stderr(capsys):
    cli._console_progress({"event": "article_start", "index": 1, "total": 1,
                           "url": "https://example.com/article"})

    output = capsys.readouterr()
    assert output.out == ""
    assert "https://example.com/article" in output.err


def test_terminal_progress_stays_at_bottom_and_highlights_errors(monkeypatch):
    class Terminal(StringIO):
        def isatty(self):
            return True

    terminal = Terminal()
    monkeypatch.setattr(cli.sys, "stderr", terminal)
    monkeypatch.setattr(cli, "_STATUS_LINE", "")
    cli._console_progress({"event": "article_start", "index": 1, "total": 10,
                           "url": "https://example.com/article"})
    cli._console_progress({"event": "error", "stage": "dataset", "error_type": "RuntimeError",
                           "error": "TEST_ONLY failure"})
    cli._console_progress({"event": "finished", "status": "partial"})
    output = terminal.getvalue()
    assert "[ 0%]" in output
    assert "\x1b[1;31m" in output and "TEST_ONLY failure" in output
    assert "[100%]" in output


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


def test_export_dataset_uses_new_path_if_previous_export_exists(monkeypatch, capsys, tmp_path):
    existing = tmp_path / "export"
    existing.mkdir()
    captured = {}
    monkeypatch.setattr(cli, "export_dataset", lambda dataset, output: (
        captured.update(output=output) or {"output": str(output)}))

    assert cli.main(["export-dataset", "dataset", "--output", str(existing)]) == 0
    assert captured["output"] != existing
    assert captured["output"].parent == existing.parent
    assert existing.is_dir()
    assert json.loads(capsys.readouterr().out)["output"] == str(captured["output"])


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
    assert json.loads(capsys.readouterr().err.splitlines()[-1])["error"] == "FileNotFoundError: dataset missing"


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


def test_collect_discovers_then_analyzes_urls_once(monkeypatch, capsys):
    captured = {}
    urls = ["https://example.test/a", "https://example.test/b"]
    def discover(config, **kwargs):
        assert kwargs["discover_only"] is True
        return {"status": "partial", "targets": [{"article_urls": urls}], "errors": []}
    monkeypatch.setattr(cli, "run_collection", discover)
    monkeypatch.setattr(cli, "load_config", lambda path: {"loaded_from": str(path)})

    def collect_dataset(config, dataset, **kwargs):
        captured.update(config=config, dataset=dataset, **kwargs)
        return {"targets_met": False, "errors": [], "counts": {"relations": 2}}

    monkeypatch.setattr(cli, "collect_dataset", collect_dataset)
    assert cli.main(["collect"]) == 2
    result = json.loads(capsys.readouterr().out)
    assert captured["urls"] == urls
    assert "from_runs" not in captured
    assert captured["dataset"] == cli._DEFAULT_DATASET
    assert captured["nodes"] == 2000
    assert captured["relations"] == 5000
    assert captured["relation_types"] == 11
    assert result["status"] == "partial"


def test_existing_schema_command_is_unchanged(capsys):
    assert cli.main(["schema"]) == 0
    assert "tables" in json.loads(capsys.readouterr().out)
