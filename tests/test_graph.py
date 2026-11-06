import pytest

from weconomy.graph import _aggregate_relations, event_edge_query, import_graph
from weconomy.pipeline import load_config, process


def test_relationship_type_not_interpolated_from_untrusted_input():
    assert "edge:ACQUIRED" in event_edge_query("ACQUIRED")
    assert "edge.triggers" in event_edge_query("ACQUIRED")
    assert "edge.rule_ids" in event_edge_query("ACQUIRED")
    with pytest.raises(ValueError):
        event_edge_query("ACQUIRED] DELETE n //")


def test_relation_edge_keeps_trigger_and_rule_provenance():
    claims = [
        {"event_id": "e", "subject_id": "a", "predicate": "INVESTED_IN", "object_id": "b",
         "assertion_status": "reported", "document_id": "d1", "source_id": "s1",
         "trigger": "invested in", "rule_id": "gliner-en-relex-v1"},
        {"event_id": "e", "subject_id": "a", "predicate": "INVESTED_IN", "object_id": "b",
         "assertion_status": "reported", "document_id": "d2", "source_id": "s2",
         "trigger": "rót vốn vào", "rule_id": "vi-investment-v1"},
    ]
    edge, = _aggregate_relations(claims)
    assert edge["claim_count"] == 2
    assert edge["document_ids"] == ["d1", "d2"]
    assert edge["triggers"] == ["invested in", "rót vốn vào"]
    assert edge["rule_ids"] == ["gliner-en-relex-v1", "vi-investment-v1"]


def test_import_writes_only_entity_nodes_and_relation_edges(tmp_path, monkeypatch):
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
    assert result["imported"].keys() == {"entities", "relations"}
    assert all("Document" not in query and "Sentence" not in query
               and "Claim" not in query and "Event" not in query and "Collection" not in query
               for query, _ in calls)
    assert any("MERGE (e:Entity" in query for query, _ in calls)
    assert any("MERGE (a)-[edge:" in query for query, _ in calls)
    entity_rows = next(rows for query, rows in calls if "MERGE (e:Entity" in query)
    assert all(set(row) <= {"entity_id", "name", "entity_type", "resolution_method"}
               for row in entity_rows)
