"""Live, read/write integration check in the local project database; no deletes."""
import argparse
import json
import os
from pathlib import Path

from neo4j import GraphDatabase

from weconomy.graph import import_graph
from weconomy.pipeline import read_table
from weconomy.quality import write_new_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    # Local generated .env stays ignored; never print credentials.
    env = Path(".env")
    if env.exists() and not os.environ.get("NEO4J_PASSWORD"):
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("NEO4J_PASSWORD="):
                os.environ["NEO4J_PASSWORD"] = line.partition("=")[2]
    datasets = {label: (key, read_table(args.run, table)) for label, key, table in (
        ("Entity", "entity_id", "entities"), ("Document", "document_id", "bronze"),
        ("Sentence", "sentence_id", "sentences"), ("Event", "event_id", "events"),
        ("Claim", "claim_id", "relations"))}
    with GraphDatabase.driver(os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                              auth=("neo4j", os.environ["NEO4J_PASSWORD"])) as driver:
        def counts():
            with driver.session(database="neo4j") as session:
                labels = {label: session.run(f"MATCH (n:{label}) RETURN count(n) AS n").single()["n"]
                          for label in ("Entity", "Document", "Sentence", "Event", "Claim")}
                labels["business_edges"] = session.run(
                    "MATCH (:Entity)-[r]->(:Entity) RETURN count(r) AS n").single()["n"]
                return labels
        initial = counts()
        first = import_graph(args.run)
        before = counts()
        second = import_graph(args.run)
        after = counts()
        if before != after:
            raise AssertionError("Reimport changed counts")
        with driver.session(database="neo4j") as session:
            scoped = {}
            for label, (key, rows) in datasets.items():
                scoped[label] = session.run(
                    f"MATCH (n:{label}) WHERE n.{key} IN $ids RETURN count(n) AS n",
                    ids=[row[key] for row in rows]).single()["n"]
                if scoped[label] != len(rows):
                    raise AssertionError(f"{label} count in Neo4j does not match run")
            event_ids = [row["event_id"] for row in datasets["Event"][1]]
            scoped["business_edges"] = session.run(
                "MATCH (:Entity)-[r]->(:Entity) WHERE r.event_id IN $ids RETURN count(r) AS n",
                ids=event_ids).single()["n"]
            if scoped["business_edges"] != len(event_ids):
                raise AssertionError("Business edge count does not match run")
            evidence = [record.data() for record in session.run("""
                MATCH (c:Claim)-[:EVIDENCED_BY]->(s:Sentence)-[:IN_DOCUMENT]->(d:Document)
                WHERE c.claim_id IN $ids
                RETURN c.predicate AS predicate, s.text AS evidence, d.url AS url,
                       d.license AS license, c.review_status AS review_status,
                       d.content_status AS content_status ORDER BY predicate
            """, ids=[row["claim_id"] for row in datasets["Claim"][1]])]
            server = session.run("CALL dbms.components() YIELD versions RETURN versions[0] AS version").single()
        result = {"neo4j_version": server["version"], "run": str(args.run),
                  "counts_before_import": initial, "run_counts": scoped,
                  "first_import": first, "second_import": second, "counts_after_first": before,
                  "counts_after_second": after, "idempotent_counts": before == after, "evidence": evidence}
        write_new_json(args.output, result)
        print(json.dumps({"run_counts": scoped, "database_counts": after,
                          "idempotent": True, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
