import pytest
import yaml

from weconomy import sources as module


def setup_config(tmp_path):
    path = tmp_path / "sources.yml"
    path.write_text(yaml.safe_dump({"sources": {
        "allowed": {"allowed": True, "kind": "news", "language": "en", "hosts": ["allowed.test"],
                    "feeds": ["https://allowed.test/rss"], "permission_basis": "local research"},
        "wikinews_en": {"allowed": False, "kind": "news", "language": "en", "hosts": ["en.wikinews.org"], "feeds": []},
        "reference": {"allowed": True, "kind": "encyclopedia_reference", "language": "vi", "hosts": ["ref.test"]},
    }}), encoding="utf-8")
    return {"sources": str(path), "min_article_words": 100}


def test_inventory_does_not_use_network_and_flags_exclusion(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "Access", lambda *_: pytest.fail("network client created"))
    result = module.source_status(setup_config(tmp_path))
    assert result["checked"] is False
    assert next(s for s in result["sources"] if s["source_id"] == "wikinews_en")["excluded"]


def test_unknown_source_raises_before_access(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "Access", lambda *_: pytest.fail("client created"))
    with pytest.raises(KeyError):
        module.source_status(setup_config(tmp_path), check=True, source_ids=["missing"])


@pytest.mark.parametrize(("title", "text", "in_scope"), [
    ("CEO announces startup acquisition", "A company acquired a startup.", True),
    ("Football final", "Team wins the match.", False),
])
def test_check_uses_access_and_extraction_interfaces_and_closes(tmp_path, monkeypatch,
                                                                 title, text, in_scope):
    config = setup_config(tmp_path)
    calls = []

    class AccessProbe:
        paused = set()
        discovery_errors = []

        def __init__(self, _config):
            calls.append("open")

        def discover_records(self, source_id, limit, *, exclude_urls=None):
            calls.append(("discover", source_id, limit))
            return [{"url": "https://allowed.test/a", "discovery_endpoint": "https://allowed.test/rss"}]

        def fetch(self, url):
            calls.append(("fetch", url))
            return {"url": url, "source_id": "allowed", "source": {"body_xpath": "//article"},
                    "body": b"page body", "headers": {"content-type": "text/html"}}

        def close(self):
            calls.append("close")

    monkeypatch.setattr(module, "Access", AccessProbe)
    monkeypatch.setattr(module, "extract_article", lambda raw, url, source, cfg: {
        "title": title, "text": text, "content_status": "body_checked",
        "nlp_eligible": True, "body_paragraphs": 2, "trafilatura_coverage": 1.0,
        "quality_flags": [],
    })
    result = module.source_status(config, check=True)
    checked = next(s for s in result["sources"] if s["source_id"] == "allowed")
    assert checked["status"] == ("eligible" if in_scope else "out_of_scope")
    assert checked["in_scope"] is in_scope
    assert "one page probe" in result["warning"].lower()
    assert not any(c[0] == "discover" and c[1] == "wikinews_en" for c in calls if isinstance(c, tuple))
    assert not any(c[0] == "discover" and c[1] == "reference" for c in calls if isinstance(c, tuple))
    assert calls[-1] == "close"


def test_empty_discovery_is_reported_and_access_closes(tmp_path, monkeypatch):
    config = setup_config(tmp_path)
    calls = []

    class EmptyAccess:
        paused = set()
        discovery_errors = []

        def __init__(self, _config):
            pass

        def discover_records(self, source_id, limit, *, exclude_urls=None):
            return []

        def fetch(self, url):
            pytest.fail("empty discovery must not fetch")

        def close(self):
            calls.append("close")

    monkeypatch.setattr(module, "Access", EmptyAccess)
    result = module.source_status(config, check=True, source_ids=["allowed"])
    assert result["sources"][0]["status"] == "unavailable"
    assert result["sources"][0]["reason"] == "No article discovered"
    assert calls == ["close"]
