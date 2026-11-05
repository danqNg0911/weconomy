import json
import re
from pathlib import Path

import pytest
import yaml

from weconomy import crawler


def test_configured_targets_use_live_allowed_sources():
    root = Path(__file__).resolve().parents[1]
    collection = yaml.safe_load((root / "config/collection.yaml").read_text(encoding="utf-8"))
    sources = yaml.safe_load((root / "config/sources.yaml").read_text(encoding="utf-8"))["sources"]
    assert len(collection["targets"]) == 6
    assert all(sources[target["source"]]["allowed"] for target in collection["targets"])
    assert {"techcrunch_venture", "techcrunch_startups"} <= {target["id"] for target in collection["targets"]}
    samples = {
        "vnexpress_world_business": "/story-123.html",
        "thanhnien_world_economy": "/story-123.htm",
        "techcrunch_venture": "/2026/11/01/company-deal/",
        "techcrunch_startups": "/2026/11/01/startup-funding/",
        "vneconomy_world_business": "/story.htm",
        "24h_world_economy": "/story-c1106a123456.html",
    }
    assert all(re.search(target["article_pattern"], samples[target["id"]])
               for target in collection["targets"])


def test_select_article_urls_is_same_host_article_pattern_and_deduplicated():
    target = "https://example.com/business/world"
    rows = [
        {"request": {"endpoint": "https://example.com/business/world"}},
        {"request": {"endpoint": "https://example.com/company-1-123.html"}},
        {"request": {"endpoint": "https://example.com/company-1-123.html?utm_source=x"}},
        {"request": {"endpoint": "https://outside.example/story-124.html"}},
        {"request": {"endpoint": "https://example.com/image.jpg"}},
    ]
    assert crawler.select_article_urls(rows, target, r"-\d+\.html$", 5) == [
        "https://example.com/company-1-123.html"]


def test_collection_load_requires_absolute_article_safety_cap(tmp_path):
    config_path = tmp_path / "collection.yaml"
    config_path.write_text("targets: []\nbatch_size: 10\n", encoding="utf-8")
    with pytest.raises(ValueError, match="targets"):
        crawler.load_collection(config_path)


def test_objective_reached_uses_all_non_null_targets():
    assert crawler.objective_reached({"articles": 2, "nodes": 100, "relations": 0},
                                     {"articles": None, "nodes": 100, "relations": None})
    assert not crawler.objective_reached({"articles": 2, "nodes": 99, "relations": 0},
                                         {"articles": None, "nodes": 100, "relations": None})


def test_katana_command_is_bounded_by_domain_pages_and_rate(tmp_path):
    args = crawler.katana_command("https://techcrunch.com/category/venture/", 12, 2)
    assert any(image.startswith("projectdiscovery/katana:") for image in args)
    assert args[args.index("-mdp") + 1] == "12"
    assert args[args.index("-c") + 1] == "1"
    assert args[args.index("-rd") + 1] == "2"
    assert args[args.index("-ct") + 1] == "30s"
    assert args[args.index("-crawl-scope") + 1] == r"https?://techcrunch\.com/category/venture/(?:[/?#]|$)"
    assert "-crawl-out-scope" in crawler.katana_command(
        "https://techcrunch.com/category/venture/", 12, 2, robots_out_scope=[r"https://techcrunch\.com/private"])
    assert crawler.katana_command("https://techcrunch.com/category/venture/", 12, 2,
                                  crawl_scope=r"https?://techcrunch\.com/category/venture/")[
                                      crawler.katana_command("https://techcrunch.com/category/venture/", 12, 2).index("-crawl-scope") + 1
                                  ] == r"https?://techcrunch\.com/category/venture/"


def test_parse_katana_jsonl_rejects_invalid_line():
    with pytest.raises(ValueError, match="Katana"):
        crawler.parse_katana_output('{"not_request": {}}')


def test_run_collection_counts_toward_node_goal_and_never_exceeds_attempt_cap(tmp_path, monkeypatch):
    config_path = tmp_path / "collection.yaml"
    source_path = tmp_path / "sources.yaml"
    source_path.write_text(yaml.safe_dump({"sources": {"fixture": {
        "hosts": ["example.test"], "allowed": True, "language": "en", "kind": "news",
        "min_interval_seconds": 0,
    }}}), encoding="utf-8")
    config_path.write_text(yaml.safe_dump({
        "version": "test", "output": "runs", "ner_backend": "gazetteer", "english_model": "en_core_web_sm",
        "aliases": "config/entities.yaml", "sources": str(source_path), "max_documents": 5,
        "max_articles": 5, "min_text_chars": 1, "min_article_words": 1, "allow_excerpts": False,
        "near_duplicate_threshold": 0.9, "request_timeout": 5, "max_response_bytes": 10000,
        "user_agent": "test", "targets": [{"id": "test", "url": "https://example.test/cat",
        "source": "fixture", "article_pattern": r"/story-\d+\.html$", "body_xpath": "//article",
        "language": "en", "max_articles": 5}], "batch_size": 2,
        "crawl": {"image": "projectdiscovery/katana:latest", "depth": 1, "delay_seconds": 1,
                  "max_pages_per_target": 20, "crawl_duration": "30s", "timeout_seconds": 2, "max_response_bytes": 4096,
                  "concurrency": 1},
        "objectives": {"articles": None, "nodes": 3, "relations": None},
    }), encoding="utf-8")
    monkeypatch.setattr(crawler, "crawl_target", lambda target, settings, **kwargs: [
        f"https://example.test/story-{i}.html" for i in range(1, 6)])
    class FakePipeline:
        calls = 0
        @staticmethod
        def process(config, *, urls, source_overrides):
            FakePipeline.calls += 1
            run = f"batch-{FakePipeline.calls}"
            article_rows = [{"canonical_url": url, "content_status": "body_checked", "duplicate_of": ""}
                            for url in urls]
            return run, {"errors": [], "article_rows": article_rows}
    monkeypatch.setattr("weconomy.pipeline.read_table", lambda run, table: (
        [] if table == "mentions" else
        [{"entity_id": f"{run}-e{i}"} for i in range(2 if run == "batch-1" else 1)]
        if table == "entities" else
        ([{"claim_id": "r1", "subject_id": f"{run}-e0", "object_id": f"{run}-e1"}]
         if run == "batch-1" else
         [{"claim_id": "r2", "subject_id": "batch-1-e0", "object_id": "batch-2-e0"}]) if table == "relations" else
        [{"canonical_url": f"https://example.test/{run}-{i}", "content_status": "body_checked", "duplicate_of": ""}
         for i in range(2)]))
    result = crawler.run_collection(config_path, process_fn=FakePipeline.process)
    assert result["objectives_met"] is True, result
    assert result["counts"]["nodes"] == 3
    assert result["counts"]["entities"] == 3
    assert result["attempted_urls"] == 4
    assert FakePipeline.calls == 2


def test_crawl_target_excludes_disallowed_robots_paths(tmp_path):
    class Rule:
        def __init__(self, path, allowance):
            self.path = path
            self.allowance = allowance
    class Entry:
        useragents = ["WeconomyResearch"]
        rulelines = [Rule("/private", False)]
        def applies_to(self, agent):
            return True
    class Robot:
        default_entry = Entry()
        entries = [Entry()]
        def can_fetch(self, agent, url):
            return "/private" not in url
    class FakeAccess:
        sources = {"fixture": {"allowed": True, "hosts": ["example.test"], "min_interval_seconds": 1}}
        def __init__(self, settings):
            self.robot = Robot()
        def policy(self, url):
            return "fixture", self.sources["fixture"]
        def robot_policy(self, origin, interval):
            return self.robot
        def close(self):
            pass
    settings = {"user_agent": "WeconomyResearch/0.1", "crawl": {
        "image": "projectdiscovery/katana:latest", "depth": 1, "delay_seconds": 1,
        "max_pages_per_target": 10, "crawl_duration": "10s", "timeout_seconds": 2,
        "max_response_bytes": 4096}}
    target = {"url": "https://example.test/category", "source": "fixture",
              "article_pattern": r"/story-\d+\.html$", "max_articles": 5}
    command = []
    output = "\n".join(json.dumps({"request": {"endpoint": url}}) for url in [
        "https://example.test/story-1.html", "https://example.test/private/story-2.html"])
    def runner(args, **kwargs):
        command.extend(args)
        return type("Result", (), {"stdout": output})()
    crawler.crawl_target(target, settings, runner=runner, access_factory=FakeAccess)
    assert "-crawl-out-scope" in command
    assert any("/private" in value for value in command)


def test_crawl_target_returns_only_robots_allowed_and_article_pattern_urls(tmp_path):
    class Robot:
        default_entry = []
        def can_fetch(self, user_agent, url):
            return "/blocked/" not in url
    class FakeAccess:
        sources = {"fixture": {"allowed": True, "hosts": ["example.test"], "min_interval_seconds": 1}}
        def __init__(self, settings):
            self.robot = Robot()
        def policy(self, url):
            return "fixture", self.sources["fixture"]
        def robot_policy(self, origin, interval):
            return self.robot
        def close(self):
            pass
    settings = {"user_agent": "WeconomyResearch/0.1", "crawl": {"image": "projectdiscovery/katana:latest", "depth": 1,
                          "delay_seconds": 1, "max_pages_per_target": 10, "crawl_duration": "30s", "timeout_seconds": 2,
                          "max_response_bytes": 4096}}
    target = {"url": "https://example.test/business", "source": "fixture",
              "article_pattern": r"/story-\d+\.html$", "max_articles": 5}
    output = "\n".join(json.dumps({"request": {"endpoint": url}}) for url in [
        "https://example.test/story-1.html", "https://example.test/blocked/story-2.html",
        "https://example.test/category"])
    urls = crawler.crawl_target(target, settings, access_factory=FakeAccess,
        runner=lambda *args, **kwargs: type("Result", (), {"stdout": output})())
    assert urls == ["https://example.test/story-1.html"]


def test_crawl_target_checks_policy_before_running_docker():
    config = {"sources": str(Path(__file__).resolve().parents[1] / "config/sources.yaml"),
              "user_agent": "test", "request_timeout": 1, "request_retries": 0,
              "max_response_bytes": 1024}
    target = {"url": "https://example.com/category", "source": "none", "max_articles": 2}
    called = []
    with pytest.raises(PermissionError, match="Source disabled"):
        crawler.crawl_target(target, config, runner=lambda *a, **k: called.append(True))
    assert called == []
