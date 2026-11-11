import pytest
import yaml

from weconomy import sources as module


def setup_config(tmp_path):
    path = tmp_path / "sources.yml"
    path.write_text(yaml.safe_dump({"sources": {
        "allowed": {"allowed": True, "kind": "news", "language": "en", "hosts": ["allowed.test"]},
        "disabled": {"allowed": False, "kind": "news", "language": "en", "hosts": ["disabled.test"]},
        "reference": {"allowed": True, "kind": "encyclopedia_reference", "language": "vi", "hosts": ["ref.test"]},
    }}), encoding="utf-8")
    return {"sources": str(path), "min_article_words": 100, "user_agent": "Test/1"}


def test_inventory_does_not_use_network_and_flags_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "Access", lambda *_: pytest.fail("network client created"))
    result = module.source_status(setup_config(tmp_path))
    assert result["checked"] is False
    assert next(s for s in result["sources"] if s["source_id"] == "disabled")["enabled"] is False


def test_unknown_source_raises_before_access(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "Access", lambda *_: pytest.fail("client created"))
    with pytest.raises(KeyError):
        module.source_status(setup_config(tmp_path), check=True, source_ids=["missing"])


def test_check_probes_policy_and_robots_only(tmp_path, monkeypatch):
    config = setup_config(tmp_path)
    calls = []

    class AccessProbe:
        paused = set()

        def __init__(self, _config):
            pass

        def policy(self, url):
            calls.append(("policy", url))

        def robot_policy(self, origin, interval):
            calls.append(("robots", origin, interval))
            return type("Robot", (), {"can_fetch": lambda *_: True})()

        def close(self):
            calls.append(("close",))

    monkeypatch.setattr(module, "Access", AccessProbe)
    result = module.source_status(config, check=True, source_ids=["allowed"])
    assert result["sources"][0]["status"] == "allowed"
    assert calls == [("policy", "https://allowed.test"),
                     ("robots", "https://allowed.test", 0), ("close",)]
    assert "does not verify article discovery" in result["warning"]
