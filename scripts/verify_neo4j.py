"""Live, read/write integration check in the local project database; no deletes."""
import argparse
import json
import os
from pathlib import Path

from neo4j import GraphDatabase

from weconomy.graph import import_graph
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
    first = import_graph(args.run)
    with GraphDatabase.driver(os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                              auth=("neo4j", os.environ["NEO4J_PASSWORD"])) as driver:
        def counts():
            with driver.session(database="neo4j") as session:
                labels = {label: session.run(f"MATCH (n:{label}) RETURN count(n) AS n").single()["n"]
                          for label in ("Entity", "Document", "Sentence", "Event", "Claim")}
                labels["business_edges"] = session.run(
                    "MATCH (:Entity)-[r]->(:Entity) RETURN count(r) AS n").single()["n"]
                return labels
        before = counts()
        second = import_graph(args.run)
        after = counts()
        if before != after:
            raise AssertionError("Reimport changed counts")
        with driver.session(database="neo4j") as session:
            evidence = [record.data() for record in session.run("""
                MATCH (c:Claim)-[:EVIDENCED_BY]->(s:Sentence)-[:IN_DOCUMENT]->(d:Document)
                RETURN c.predicate AS predicate, s.text AS evidence, d.url AS url,
                       d.license AS license, c.review_status AS review_status ORDER BY predicate
            """)]
            server = session.run("CALL dbms.components() YIELD versions RETURN versions[0] AS version").single()
        result = {"neo4j_version": server["version"], "run": str(args.run),
                  "first_import": first, "second_import": second, "counts_after_first": before,
                  "counts_after_second": after, "idempotent_counts": before == after, "evidence": evidence}
        write_new_json(args.output, result)
        print(json.dumps({"counts": after, "idempotent": True, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
