"""Refresh the public graph files directly from the configured Neo4j AuraDB."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import ssl
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from neo4j import GraphDatabase, READ_ACCESS


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "public-data" / "v15-global-business-only-20261112"
SIDECAR_SOURCE_EXPORT = "international-business-v15-manual-20261112-global-business-only"
SIDECAR_SOURCE_MANIFEST_SHA256 = "6e69d2cf80e9a93835538e4cfdc0b9af82850e555fa3312edaf820eaef1158f7"


def load_root_env() -> dict[str, str]:
    values = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.removeprefix("export ").split("=", 1)
            values[key.strip()] = value.strip().strip("\"'").strip()
    return values


def read_jsonl_count(path: Path) -> int:
    with path.open(encoding="utf-8") as stream:
        return sum(1 for line in stream if line.strip())


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def fetch_aura_graph() -> tuple[str, list[dict], list[dict]]:
    config = load_root_env()
    uri = config.get("NEO4J_URI", "")
    password = config.get("NEO4J_PASSWORD", "")
    if not uri or not password:
        raise RuntimeError("Root .env must define NEO4J_URI and NEO4J_PASSWORD")
    username = config.get("NEO4J_USERNAME") or config.get("NEO4J_USER") or "neo4j"
    database = config.get("NEO4J_DATABASE") or "neo4j"

    ca_path = os.getenv("NEO4J_CA_CERT")
    if ca_path:
        parsed = urlparse(uri)
        context = ssl.create_default_context()
        context.load_verify_locations(cafile=ca_path)
        driver_uri = f"neo4j://{parsed.hostname}:{parsed.port or 7687}"
        driver_options = {"ssl_context": context}
    else:
        driver_uri = uri
        driver_options = {}

    with GraphDatabase.driver(driver_uri, auth=(username, password), **driver_options) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode=READ_ACCESS) as session:
            entity_rows = [
                dict(row["properties"])
                for row in session.run("MATCH (n:Entity) RETURN properties(n) AS properties ORDER BY n.entity_id")
            ]
            relation_rows = []
            for row in session.run(
                "MATCH (a:Entity)-[r]->(b:Entity) "
                "RETURN a.entity_id AS subject_id, type(r) AS predicate, "
                "b.entity_id AS object_id, properties(r) AS properties "
                "ORDER BY subject_id, predicate, object_id, properties.relation_id"
            ):
                relation = {
                    "subject_id": row["subject_id"],
                    "predicate": row["predicate"],
                    "object_id": row["object_id"],
                    **dict(row["properties"]),
                }
                relation_rows.append(relation)
    return database, entity_rows, relation_rows


def build(destination: Path = DESTINATION) -> dict:
    destination = destination.resolve()
    old_manifest_path = destination / "manifest.json"
    old_manifest = json.loads(old_manifest_path.read_text(encoding="utf-8"))
    database, entities, relations = fetch_aura_graph()
    entity_ids = {row["entity_id"] for row in entities}
    endpoints = {row[key] for row in relations for key in ("subject_id", "object_id")}
    if not endpoints <= entity_ids:
        raise ValueError("Aura relationship endpoint is missing from the Entity node export")

    claim_ids = {row["claim_id"] for row in read_jsonl(destination / "claims.jsonl")}
    article_ids = {row["document_id"] for row in read_jsonl(destination / "articles.jsonl")}
    aura_claim_ids = {
        claim_id
        for row in relations
        for event in json.loads(row.get("event_details_json") or "[]")
        for claim_id in event.get("claim_ids", [])
    }
    aura_document_ids = {
        document_id
        for row in relations
        for document_id in row.get("document_ids", [])
    }
    if aura_claim_ids != claim_ids or not aura_document_ids <= article_ids:
        raise ValueError("Public claims/articles sidecars do not cover the claim/document IDs stored in AuraDB")

    destination.mkdir(parents=True, exist_ok=True)
    entity_path = destination / "entities.jsonl"
    relation_path = destination / "relations.jsonl"
    entity_tmp = destination / "entities.jsonl.tmp"
    relation_tmp = destination / "relations.jsonl.tmp"
    write_jsonl(entity_tmp, entities)
    write_jsonl(relation_tmp, relations)
    entity_tmp.replace(entity_path)
    relation_tmp.replace(relation_path)

    articles_count = read_jsonl_count(destination / "articles.jsonl")
    claims_count = read_jsonl_count(destination / "claims.jsonl")
    relation_types = len({row["predicate"] for row in relations})
    graph_fingerprint = hashlib.sha256(
        "\n".join([
            *(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in entities),
            *(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in relations),
        ]).encode("utf-8")
    ).hexdigest()
    old_source_counts = old_manifest.get("source_counts", {})
    old_counts = old_manifest.get("counts", {})
    source_counts = {
        "entity_rows": old_source_counts.get("entity_rows", old_counts.get("entities", len(entities))),
        "isolated_entities_omitted": old_source_counts.get(
            "isolated_entities_omitted", max(0, old_counts.get("entities", len(entities)) - len(entities))
        ),
    }
    manifest = {
        "release": old_manifest.get("release", "v15-global-business-only-20261112"),
        "aura_snapshot": {
            "database": database,
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "entity_label": "Entity",
            "relationship_scope": "all directed relationships whose endpoints are Entity nodes",
            "graph_sha256": graph_fingerprint,
        },
        "counts": {
            "articles": articles_count,
            "entities": len(entities),
            "nodes": len(entities),
            "isolated_entities": len(entity_ids - endpoints),
            "relations": len(relations),
            "claims": claims_count,
            "relation_types": relation_types,
        },
        "source_counts": source_counts,
        "supporting_sidecars": {
            "source_export": old_manifest.get("source_export") or SIDECAR_SOURCE_EXPORT,
            "source_export_manifest_sha256": old_manifest.get("source_export_manifest_sha256") or SIDECAR_SOURCE_MANIFEST_SHA256,
            "note": "articles.jsonl and claims.jsonl are text-free supporting files, not AuraDB nodes; every Aura claim ID is covered and every linked document ID is present.",
        },
        "file_sha256": {
            name: sha256(destination / name)
            for name in ("articles.jsonl", "claims.jsonl", "entities.jsonl", "relations.jsonl")
        },
        "public_projection": {
            "graph_files": "entities.jsonl and relations.jsonl are direct AuraDB node and relationship property exports",
            "sidecar_evidence_status": "article text and evidence quotes are omitted; use the group's access-controlled evidence bundle",
            "quality_status": "candidate graph; independent human-gold precision has not been measured",
        },
    }
    manifest_path = destination / "manifest.json"
    manifest_tmp = destination / "manifest.json.tmp"
    manifest_tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_tmp.replace(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DESTINATION)
    args = parser.parse_args()
    manifest = build(args.out)
    print(json.dumps({"output": str(args.out.resolve()), "counts": manifest["counts"]}, indent=2))


if __name__ == "__main__":
    main()
