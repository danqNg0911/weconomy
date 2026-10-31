"""Parameterized, transactional, idempotent Neo4j import. No deletes."""
import os

from neo4j import GraphDatabase

from .pipeline import read_table
from .schema import RELATION_TYPES

CONSTRAINTS = [f"CREATE CONSTRAINT {label.lower()}_id IF NOT EXISTS FOR (n:{label}) REQUIRE n.{key} IS UNIQUE"
               for label, key in [("Entity", "entity_id"), ("Document", "document_id"),
                                   ("Sentence", "sentence_id"), ("Claim", "claim_id"), ("Event", "event_id")]]

QUERIES = {
    "entities": "UNWIND $rows AS r MERGE (e:Entity {entity_id:r.entity_id}) SET e += r",
    "bronze": """UNWIND $rows AS r MERGE (d:Document {document_id:r.document_id})
        SET d.url=r.url, d.source_id=r.source_id, d.license=r.license, d.attribution=r.attribution,
            d.published_at=r.published_at, d.retrieved_at=r.retrieved_at, d.kind=r.kind, d.raw_sha256=r.raw_sha256""",
    "sentences": """UNWIND $rows AS r MATCH (d:Document {document_id:r.document_id})
        MERGE (s:Sentence {sentence_id:r.sentence_id}) SET s += r MERGE (s)-[:IN_DOCUMENT]->(d)""",
    "events": """UNWIND $rows AS r
        MATCH (a:Entity {entity_id:r.subject_id}), (b:Entity {entity_id:r.object_id})
        MERGE (e:Event {event_id:r.event_id}) SET e += r
        MERGE (e)-[:SUBJECT]->(a) MERGE (e)-[:OBJECT]->(b)""",
    "relations": """UNWIND $rows AS r MATCH (e:Event {event_id:r.event_id}),
        (s:Sentence {sentence_id:r.sentence_id})
        MERGE (c:Claim {claim_id:r.claim_id})
        WITH c, r, e, s, c.review_status AS previous_status
        SET c += r SET c.review_status=coalesce(previous_status, r.review_status)
        MERGE (c)-[:ABOUT_EVENT]->(e) MERGE (c)-[:EVIDENCED_BY]->(s)""",
}


def event_edge_query(predicate):
    if predicate not in RELATION_TYPES:
        raise ValueError("Invalid relation type")
    return f"""UNWIND $rows AS r MATCH (a:Entity {{entity_id:r.subject_id}}),
        (b:Entity {{entity_id:r.object_id}})
        MERGE (a)-[edge:{predicate} {{event_id:r.event_id}}]->(b)
        SET edge.assertion_status=r.assertion_status, edge.review_status=coalesce(edge.review_status,'unreviewed'),
            edge.event_date=r.event_date"""


def import_graph(run, batch_size=500):
    from .quality import validate
    validation = validate(run)
    if not validation["valid"]:
        raise ValueError(f"Invalid graph dataset: {validation['failures']}")
    password = os.environ.get("NEO4J_PASSWORD")
    if not password:
        raise ValueError("Set NEO4J_PASSWORD in your environment before importing")
    tables = {name: read_table(run, name) for name in QUERIES}
    with GraphDatabase.driver(os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                              auth=(os.getenv("NEO4J_USER", "neo4j"), password)) as driver:
        driver.verify_connectivity()
        with driver.session(database="neo4j") as session:
            for query in CONSTRAINTS:
                session.run(query).consume()

            def write(tx):
                for name, query in QUERIES.items():
                    rows = tables[name]
                    for offset in range(0, len(rows), batch_size):
                        tx.run(query, rows=rows[offset:offset+batch_size]).consume()
                for predicate in RELATION_TYPES:
                    rows = [r for r in tables["events"] if r["predicate"] == predicate]
                    for offset in range(0, len(rows), batch_size):
                        tx.run(event_edge_query(predicate), rows=rows[offset:offset+batch_size]).consume()
            session.execute_write(write)
    return {"imported": {key: len(value) for key, value in tables.items()}, "run": str(run)}
