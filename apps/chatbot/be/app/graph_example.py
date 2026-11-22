"""Fixed, read-only AuraDB example for the graph viewport."""

from fastapi import HTTPException
from neo4j import GraphDatabase, unit_of_work

from .config import Settings
from .evidence import enrich
from .graph_rag import edge_data, edge_evidence

QUERY = """
MATCH p=(seed:Entity {name: $name})-[*1..2]-(other:Entity)
WHERE other <> seed AND all(n IN nodes(p) WHERE n:Entity)
RETURN p
LIMIT 6
"""


def load_example(settings: Settings):
    if not settings.neo4j_uri or not settings.neo4j_password.get_secret_value():
        raise HTTPException(503, "Thiếu cấu hình Neo4j phía backend.")

    @unit_of_work(timeout=10)
    def read(tx):
        nodes, edges, evidence = {}, {}, {}
        for record in tx.run(QUERY, name="TDK Ventures"):
            path = record["p"]
            for node in path.nodes:
                nodes[node.element_id] = {
                    "id": node.element_id,
                    "label": str(node.get("name") or node.element_id),
                    "type": str(node.get("entity_type") or "Entity"),
                }
            for edge in path.relationships:
                edges[edge.element_id] = edge_data(edge)
                evidence[edge.element_id] = edge_evidence(edge)
        return {
            "nodes": list(nodes.values()),
            "edges": list(edges.values()),
            "evidence": [item for items in evidence.values() for item in items],
        }

    try:
        with GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_username or settings.neo4j_user, settings.neo4j_password.get_secret_value()),
            connection_timeout=10,
            connection_acquisition_timeout=15,
            max_transaction_retry_time=0,
        ) as driver:
            with driver.session(database=settings.neo4j_database, default_access_mode="READ") as session:
                details = enrich(settings, {"graph": session.execute_read(read), "metadata": {}})
                return {**details, "name": "TDK Ventures", "query": QUERY}
    except Exception as exc:
        raise HTTPException(502, "Không tải được graph AuraDB. Kiểm tra kết nối Neo4j phía backend.") from exc
