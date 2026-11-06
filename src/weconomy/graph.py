"""Parameterized, transactional, idempotent Neo4j import. No deletes."""
import json
import os
from pathlib import Path

from neo4j import GraphDatabase

from .pipeline import read_table

CONSTRAINTS = ["CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (n:Entity) REQUIRE n.entity_id IS UNIQUE"]
ENTITY_PROPERTIES = ("entity_id", "name", "entity_type", "resolution_method", "domain_types")

QUERIES = {
    "entities": """UNWIND $rows AS r MERGE (e:Entity {entity_id:r.entity_id}) SET e += r
        SET e.collection_ids = CASE WHEN $collection_id IN coalesce(e.collection_ids, [])
            THEN coalesce(e.collection_ids, []) ELSE coalesce(e.collection_ids, []) + [$collection_id] END""",
}


def event_edge_query(predicate):
    if not isinstance(predicate, str) or not predicate.isidentifier() or predicate.upper() != predicate:
        raise ValueError("Invalid relation type")
    return f"""UNWIND $rows AS r MATCH (a:Entity {{entity_id:r.subject_id}}),
        (b:Entity {{entity_id:r.object_id}})
        MERGE (a)-[edge:{predicate} {{event_id:r.event_id}}]->(b)
        SET edge.assertion_status=r.assertion_status,
            edge.review_status=coalesce(edge.review_status, r.review_status, 'unreviewed'),
            edge.event_date=r.event_date, edge.document_ids=coalesce(r.document_ids, []),
            edge.source_ids=coalesce(r.source_ids, []), edge.claim_count=coalesce(r.claim_count, 0)
        SET edge.triggers=coalesce(r.triggers, []), edge.rule_ids=coalesce(r.rule_ids, [])
        SET edge.collection_ids = CASE WHEN $collection_id IN coalesce(edge.collection_ids, [])
            THEN coalesce(edge.collection_ids, []) ELSE coalesce(edge.collection_ids, []) + [$collection_id] END"""


def _aggregate_relations(claims, events=()):
    grouped = {row["event_id"]: {**row, "document_ids": [], "source_ids": [],
                                  "triggers": [], "rule_ids": [], "claim_count": 0}
               for row in events}
    for claim in claims:
        event = grouped.setdefault(claim["event_id"], {
            "event_id": claim["event_id"], "subject_id": claim["subject_id"],
            "predicate": claim["predicate"], "object_id": claim["object_id"],
            "assertion_status": claim["assertion_status"], "event_date": claim.get("event_date", ""),
            "dedup_scope": "within_document_unknown_date", "document_ids": [], "source_ids": [],
            "triggers": [], "rule_ids": [], "claim_count": 0,
        })
        event["document_ids"].append(claim.get("document_id", ""))
        event["source_ids"].append(claim.get("source_id", ""))
        event["triggers"].append(claim.get("trigger", ""))
        event["rule_ids"].append(claim.get("rule_id", ""))
        event["claim_count"] += 1
    for event in grouped.values():
        for key in ("document_ids", "source_ids", "triggers", "rule_ids"):
            event[key] = sorted({value for value in event[key] if value})
    return list(grouped.values())


def _read_export(folder):
    manifest = json.loads((folder / "manifest.json").read_text("utf-8"))
    files = {name: folder / f"{name}.jsonl" for name in ("articles", "entities", "relations", "claims")}
    if any(not path.is_file() for path in files.values()):
        raise ValueError("Dataset export requires articles, entities, relations, claims and manifest files")
    rows = {name: [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]
            for name, path in files.items()}
    counts = manifest.get("counts", {})
    if (len(rows["articles"]) != counts.get("articles")
            or len(rows["entities"]) != counts.get("nodes")
            or len(rows["relations"]) != counts.get("relations")
            or len(rows["claims"]) != counts.get("claims")):
        raise ValueError("Dataset export counts do not match manifest")

    article_ids = {row["document_id"] for row in rows["articles"]}
    events = []
    for claim in rows["claims"]:
        if claim["document_id"] not in article_ids:
            raise ValueError(f"Claim references an unexported document: {claim['document_id']}")
    events = _aggregate_relations(rows["claims"])
    entities = [{key: entity[key] for key in ENTITY_PROPERTIES if key in entity}
                for entity in rows["entities"]]
    return {"entities": entities, "events": events}


def import_graph(run, batch_size=500):
    run = Path(run)
    if (run / "articles.jsonl").is_file():
        tables = _read_export(run)
    else:
        from .quality import validate
        validation = validate(run)
        if not validation["valid"]:
            raise ValueError(f"Invalid graph dataset: {validation['failures']}")
        tables = {"entities": [{key: entity[key] for key in ENTITY_PROPERTIES if key in entity}
                                for entity in read_table(run, "entities")],
                  "events": _aggregate_relations(read_table(run, "relations"), read_table(run, "events"))}
    collection_id = run.name
    password = os.environ.get("NEO4J_PASSWORD")
    if not password:
        raise ValueError("Set NEO4J_PASSWORD in your environment before importing")
    with GraphDatabase.driver(os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                              auth=(os.getenv("NEO4J_USERNAME", os.getenv("NEO4J_USER", "neo4j")), password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=os.getenv("NEO4J_DATABASE", "neo4j")) as session:
            for query in CONSTRAINTS:
                session.run(query).consume()
            def write(tx):
                for name, query in QUERIES.items():
                    rows = tables[name]
                    for offset in range(0, len(rows), batch_size):
                        tx.run(query, rows=rows[offset:offset+batch_size], collection_id=collection_id).consume()
                for predicate in sorted({r["predicate"] for r in tables["events"]}):
                    rows = [r for r in tables["events"] if r["predicate"] == predicate]
                    for offset in range(0, len(rows), batch_size):
                        tx.run(event_edge_query(predicate), rows=rows[offset:offset+batch_size],
                               collection_id=collection_id).consume()
            session.execute_write(write)
    return {"collection_id": collection_id,
            "imported": {"entities": len(tables["entities"]), "relations": len(tables["events"])},
            "source": str(run)}
