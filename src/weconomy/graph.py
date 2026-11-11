"""Parameterized, transactional, idempotent Neo4j import. No deletes."""
import json
import os
from pathlib import Path

from neo4j import GraphDatabase

from .pipeline import read_table
from .schema import SYMMETRIC_RELATIONS, stable_id

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
        MERGE (a)-[edge:{predicate} {{relation_id:r.relation_id, collection_id:$collection_id}}]->(b)
        SET edge.assertion_status=r.assertion_status,
            edge.review_status=r.review_status, edge.review_statuses=r.review_statuses,
            edge.event_date=r.event_date, edge.document_ids=r.document_ids,
            edge.source_ids=r.source_ids, edge.event_ids=r.event_ids,
            edge.event_count=r.event_count, edge.claim_count=r.claim_count,
            edge.event_details_json=r.event_details_json,
            edge.triggers=r.triggers, edge.rule_ids=r.rule_ids,
            edge.collection_ids=[$collection_id]"""


def _aggregate_relations(claims, events=()):
    grouped = {}

    def get_group(row):
        subject, predicate, object_ = row["subject_id"], row["predicate"], row["object_id"]
        if predicate in SYMMETRIC_RELATIONS and subject > object_:
            subject, object_ = object_, subject
        key = (subject, predicate, object_)
        return grouped.setdefault(key, {
            "relation_id": stable_id(*key), "subject_id": subject, "predicate": predicate,
            "object_id": object_, "document_ids": set(), "source_ids": set(), "triggers": set(),
            "rule_ids": set(), "review_statuses": set(), "assertion_statuses": set(),
            "_events": {}, "_claims": set(),
        })

    for event in events:
        group = get_group(event)
        event_id = event["event_id"]
        group["_events"].setdefault(event_id, {
            "event_id": event_id, "assertion_status": event.get("assertion_status", ""),
            "event_date": event.get("event_date", ""),
            "dedup_scope": event.get("dedup_scope", "within_document_unknown_date"),
            "document_ids": set(), "claim_ids": set(),
        })

    for claim in claims:
        group = get_group(claim)
        event_id = claim.get("event_id") or stable_id(
            claim["subject_id"], claim["predicate"], claim["object_id"], claim.get("document_id", ""),
        )
        event = group["_events"].setdefault(event_id, {
            "event_id": event_id, "assertion_status": claim.get("assertion_status", ""),
            "event_date": claim.get("event_date", ""),
            "dedup_scope": "within_document_unknown_date", "document_ids": set(), "claim_ids": set(),
        })
        claim_key = claim.get("claim_id") or (
            event_id, claim.get("document_id"), claim.get("sentence_id"),
            claim.get("trigger"), claim.get("rule_id"),
        )
        if claim_key in group["_claims"]:
            continue
        group["_claims"].add(claim_key)
        for key, target in (("document_id", "document_ids"), ("source_id", "source_ids"),
                            ("trigger", "triggers"), ("rule_id", "rule_ids")):
            if claim.get(key):
                group[target].add(claim[key])
        group["review_statuses"].add(claim.get("review_status", "unreviewed"))
        if claim.get("assertion_status"):
            group["assertion_statuses"].add(claim["assertion_status"])
        if claim.get("document_id"):
            event["document_ids"].add(claim["document_id"])
        if claim.get("claim_id"):
            event["claim_ids"].add(claim["claim_id"])

    result = []
    for group in grouped.values():
        events_by_id = group.pop("_events")
        claims_seen = group.pop("_claims")
        for key in ("document_ids", "source_ids", "triggers", "rule_ids", "review_statuses",
                    "assertion_statuses"):
            group[key] = sorted(group[key])
        group["event_ids"] = sorted(events_by_id)
        event_details = [{key: sorted(value) if isinstance(value, set) else value
                          for key, value in sorted(event.items())} for event in events_by_id.values()]
        group["event_details_json"] = json.dumps(event_details, ensure_ascii=False, sort_keys=True)
        group["event_count"] = len(events_by_id)
        group["claim_count"] = len(claims_seen)
        group["review_status"] = (group["review_statuses"][0] if len(group["review_statuses"]) == 1
                                  else "mixed" if group["review_statuses"] else "unreviewed")
        group["assertion_status"] = (
            group["assertion_statuses"][0] if len(group["assertion_statuses"]) == 1
            else "mixed" if group["assertion_statuses"] else "reported")
        event_dates = {event["event_date"] for event in events_by_id.values() if event["event_date"]}
        group["event_date"] = next(iter(event_dates)) if len(event_dates) == 1 else ""
        result.append(group)
    return result


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
