import pytest

from weconomy.graph import event_edge_query, import_graph
from weconomy.pipeline import load_config, process


def test_relationship_type_not_interpolated_from_untrusted_input():
    assert "edge:ACQUIRED" in event_edge_query("ACQUIRED")
    with pytest.raises(ValueError):
        event_edge_query("ACQUIRED] DELETE n //")


def test_import_sends_content_gate_metadata_without_raw_html(tmp_path, monkeypatch):
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "config/pipeline.yaml")
    config.update(output=str(tmp_path / "runs"), allow_excerpts=True)
    run, _ = process(config, manifest=root / "samples/excerpts/manifest.json")
    calls = []

    class Driver:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def verify_connectivity(self):
            pass

        def session(self, **kwargs):
            return self

        def run(self, query, **kwargs):
            calls.append((query, kwargs.get("rows", [])))
            return self

        def consume(self):
            pass

        def execute_write(self, action):
            action(self)

    monkeypatch.setenv("NEO4J_PASSWORD", "unit-test-only")
    monkeypatch.setattr("weconomy.graph.GraphDatabase.driver", lambda *a, **k: Driver())
    result = import_graph(run)
    documents = next(rows for query, rows in calls if "MERGE (d:Document" in query)
    assert len(documents) == result["imported"]["bronze"] == 4
    assert all(d["content_status"] == "excerpt" and d["nlp_eligible"] for d in documents)
    assert all("raw_bytes" not in d and "raw_html" not in d for d in documents)
