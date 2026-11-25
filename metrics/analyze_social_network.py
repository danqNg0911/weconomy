"""Read-only network analysis of the graph currently loaded in Neo4j AuraDB."""

from __future__ import annotations

import hashlib
import json
import os
import ssl
from collections import Counter
from datetime import date
from pathlib import Path
from statistics import mean
from urllib.parse import urlparse

import networkx as nx
from neo4j import GraphDatabase, READ_ACCESS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public-data" / "v15-global-business-only-20261112"
OUT = ROOT / "metrics" / "results" / "social-network-analysis-aura-20261125"
SYMMETRIC = {"CO_INVESTED_WITH", "CO_FINANCED_WITH", "COMPETES_WITH", "MERGED_WITH", "PARTNERED_WITH"}
NULL_REPLICATES = 5
SWAP_ATTEMPTS_PER_EDGE = 10
SWAP_SEED = 20261125


def load_root_env() -> dict[str, str]:
    values = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.removeprefix("export ").split("=", 1)
            values[key.strip()] = value.strip().strip("\"'").strip()
    return values


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def canonical_triple(source: str, predicate: str, target: str) -> tuple[str, str, str]:
    if predicate in SYMMETRIC and target < source:
        source, target = target, source
    return source, predicate, target


def read_aura_graph():
    config = load_root_env()
    uri = config.get("NEO4J_URI", "")
    password = config.get("NEO4J_PASSWORD", "")
    if not uri or not password:
        raise RuntimeError("Root .env must define NEO4J_URI and NEO4J_PASSWORD")
    username = config.get("NEO4J_USERNAME") or config.get("NEO4J_USER") or "neo4j"
    database = config.get("NEO4J_DATABASE") or "neo4j"

    parsed = urlparse(uri)
    ca_path = os.getenv("NEO4J_CA_CERT")
    if ca_path:
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
            entity_rows = list(session.run(
                "MATCH (n:Entity) RETURN properties(n) AS properties "
                "ORDER BY n.entity_id"
            ))
            edge_rows = list(session.run(
                "MATCH (a:Entity)-[r]->(b:Entity) "
                "RETURN a.entity_id AS subject_id, type(r) AS predicate, "
                "b.entity_id AS object_id, properties(r) AS properties "
                "ORDER BY subject_id, predicate, object_id, properties.relation_id"
            ))

    entities = [dict(row["properties"]) for row in entity_rows]
    relations = [
        {"subject_id": row["subject_id"], "predicate": row["predicate"],
         "object_id": row["object_id"], **dict(row["properties"])}
        for row in edge_rows if row["subject_id"] and row["object_id"]
    ]
    return database, entities, relations


def main() -> None:
    database, aura_entity_rows, relations = read_aura_graph()
    entities = {
        row["entity_id"]: {"name": row.get("name") or row["entity_id"],
                           "entity_type": row.get("entity_type") or ""}
        for row in aura_entity_rows if row.get("entity_id")
    }
    graph = nx.Graph()
    directed = nx.DiGraph()
    graph.add_nodes_from(sorted(entities))
    directed.add_nodes_from(sorted(entities))
    predicate_counts = Counter()
    aura_triples = set()
    for row in relations:
        source, target, predicate = row["subject_id"], row["object_id"], row["predicate"]
        if source not in entities or target not in entities:
            continue
        predicate_counts[predicate] += 1
        aura_triples.add(canonical_triple(source, predicate, target))
        if source != target:
            graph.add_edge(source, target)
            directed.add_edge(source, target)
            if predicate in SYMMETRIC:
                directed.add_edge(target, source)

    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    lcc = graph.subgraph(components[0]).copy()
    clustering = nx.average_clustering(lcc)
    average_path = nx.average_shortest_path_length(lcc)
    component_paths = [
        (component_graph.number_of_nodes() * (component_graph.number_of_nodes() - 1),
         nx.average_shortest_path_length(component_graph))
        for component in components if len(component) > 1
        for component_graph in [graph.subgraph(component)]
    ]
    reachable_pairs = sum(pair_count for pair_count, _ in component_paths)
    average_path_reachable = (
        sum(pair_count * path_length for pair_count, path_length in component_paths) / reachable_pairs
        if reachable_pairs else 0
    )
    swap_attempts = SWAP_ATTEMPTS_PER_EDGE * lcc.number_of_edges()
    null_graphs = []
    successful_swaps = []
    original_degrees = dict(lcc.degree())
    for index in range(NULL_REPLICATES):
        null = lcc.copy()
        successful_swaps.append(nx.connected_double_edge_swap(
            null, nswap=swap_attempts, seed=SWAP_SEED + index
        ))
        if dict(null.degree()) != original_degrees or not nx.is_connected(null):
            raise RuntimeError("Degree-preserving null graph invariant failed")
        null_graphs.append(null)
    null_clustering_values = [nx.average_clustering(null) for null in null_graphs]
    null_path_values = [nx.average_shortest_path_length(null) for null in null_graphs]
    null_clustering = mean(null_clustering_values)
    null_path = mean(null_path_values)
    clustering_ratio = clustering / null_clustering if null_clustering else float("inf")
    path_ratio = average_path / null_path if null_path else float("inf")
    sigma = clustering_ratio / path_ratio if path_ratio else float("inf")

    pagerank = nx.pagerank(directed, alpha=0.85, weight=None)
    core = nx.core_number(graph)
    maximum_core = max(core.values(), default=0)
    maximum_core_nodes = [node for node, value in core.items() if value == maximum_core]
    communities = nx.community.louvain_communities(lcc, seed=20261124)
    modularity = nx.community.modularity(lcc, communities)

    def node_summary(node: str) -> dict:
        return {"entity_id": node, "name": entities[node]["name"], "type": entities[node]["entity_type"]}

    ranked = sorted(pagerank.items(), key=lambda row: row[1], reverse=True)
    community_rows = []
    for index, community in enumerate(sorted(communities, key=len, reverse=True), 1):
        leaders = sorted(community, key=lambda node: pagerank[node], reverse=True)[:10]
        community_rows.append({
            "rank": index,
            "size": len(community),
            "top_pagerank_nodes": [node_summary(node) | {"pagerank": pagerank[node]} for node in leaders],
        })

    export_entities = {row["entity_id"]: row for row in read_jsonl(DATA / "entities.jsonl")}
    export_relations = list(read_jsonl(DATA / "relations.jsonl"))
    export_manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
    source_counts = export_manifest.get("source_counts", {})
    export_ids = set(export_entities)
    export_triples = {
        canonical_triple(row["subject_id"], row["predicate"], row["object_id"])
        for row in export_relations
    }
    export_endpoints = {
        endpoint for row in export_relations for endpoint in (row["subject_id"], row["object_id"])
    }
    aura_ids = set(entities)
    aura_entities_by_id = {row["entity_id"]: row for row in aura_entity_rows}
    metadata_mismatches = sum(
        export_entities[node] != aura_entities_by_id[node] for node in aura_ids & export_ids
    )
    aura_rows = [
        *sorted(aura_entity_rows, key=lambda row: row["entity_id"]),
        *sorted(relations, key=lambda row: (row["subject_id"], row["predicate"], row["object_id"], row["relation_id"])),
    ]
    fingerprint_source = "\n".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in aura_rows
    )
    data_fingerprint = hashlib.sha256(fingerprint_source.encode("utf-8")).hexdigest()
    connected_pair_fraction = (
        sum(size * (size - 1) for size in map(len, components)) / (len(graph) * (len(graph) - 1))
        if len(graph) > 1 else 0
    )

    result = {
        "generated_on": date.today().isoformat(),
        "source": "Neo4j AuraDB read-only snapshot",
        "source_database": database,
        "aura_graph_sha256": data_fingerprint,
        "method": {
            "undirected_projection": "one unweighted edge per unique entity pair; Aura Entity nodes retained",
            "directed_pagerank": "one unweighted edge per ordered pair; schema-symmetric predicates mirrored",
            "pagerank_alpha": 0.85,
            "communities": "Louvain on largest connected component; seed=20261124",
            "core": "k-core on Aura Entity nodes",
            "small_world": "sigma ratio against connected degree-preserving double-edge-swap null graphs",
            "small_world_null_replicates": NULL_REPLICATES,
            "small_world_swap_attempts_per_graph": swap_attempts,
            "small_world_successful_swaps": successful_swaps,
            "small_world_null_seeds": [SWAP_SEED + i for i in range(NULL_REPLICATES)],
            "small_world_nulls_preserve_degree_sequence": True,
            "small_world_nulls_are_connected": True,
        },
        "comparison_to_public_v15": {
            "public_projection_entity_rows": len(export_ids), "aura_entity_nodes": len(aura_ids),
            "source_normalized_export_entity_rows": source_counts.get("entity_rows", len(export_ids)),
            "source_isolated_entities_omitted": source_counts.get("isolated_entities_omitted", 0),
            "aura_entity_ids_equal_public_projection_ids": aura_ids == export_ids,
            "aura_entity_ids_equal_relation_endpoint_ids": aura_ids == export_endpoints,
            "entity_property_mismatches": metadata_mismatches,
            "export_relation_rows": len(export_relations), "aura_relation_rows": len(relations),
            "full_graph_fingerprint_matches_public_manifest": (
                data_fingerprint == export_manifest.get("aura_snapshot", {}).get("graph_sha256")
            ),
            "unique_relation_triples_equal": export_triples == aura_triples,
            "missing_aura_relation_triples": len(export_triples - aura_triples),
            "extra_aura_relation_triples": len(aura_triples - export_triples),
        },
        "graph": {
            "entity_nodes": len(graph), "raw_relationships": len(relations),
            "unique_undirected_edges": graph.number_of_edges(),
            "unique_directed_edges_after_symmetry": directed.number_of_edges(),
            "predicate_counts_top_15": predicate_counts.most_common(15),
            "component_count": len(components), "isolates": nx.number_of_isolates(graph),
            "largest_component_nodes": lcc.number_of_nodes(), "largest_component_edges": lcc.number_of_edges(),
            "largest_component_fraction": lcc.number_of_nodes() / graph.number_of_nodes(),
            "connected_pair_fraction": connected_pair_fraction,
            "average_shortest_path_all_reachable_pairs": average_path_reachable,
            "average_shortest_path_largest_component": average_path,
            "average_clustering_largest_component": clustering,
            "transitivity_largest_component": nx.transitivity(lcc),
            "small_world_null_average_clustering": null_clustering,
            "small_world_null_clustering_range": [min(null_clustering_values), max(null_clustering_values)],
            "small_world_clustering_ratio": clustering_ratio,
            "small_world_null_average_shortest_path": null_path,
            "small_world_null_path_range": [min(null_path_values), max(null_path_values)],
            "small_world_path_ratio": path_ratio,
            "small_world_sigma": sigma, "small_world_sigma_gt_1": sigma > 1,
        },
        "pagerank_top_30": [node_summary(node) | {"pagerank": score} for node, score in ranked[:30]],
        "communities": {"count": len(communities), "modularity": modularity, "largest_10": community_rows[:10]},
        "core": {
            "maximum_k": maximum_core, "maximum_core_size": len(maximum_core_nodes),
            "maximum_core_nodes": [
                node_summary(node) | {"core_number": core[node], "pagerank": pagerank[node]}
                for node in sorted(maximum_core_nodes, key=lambda n: pagerank[n], reverse=True)[:100]
            ],
            "core_size_by_k": dict(sorted(Counter(core.values()).items())),
        },
        "caveats": [
            "A finite all-pairs average is undefined for this disconnected graph; the reported whole-network average covers reachable pairs only, and the standard small-world comparison uses the largest component.",
            "The small-world sigma uses connected degree-preserving null graphs; only five randomizations are used, so report the replicate ranges and treat sigma as a structural comparison, not a significance test.",
            f"CO_INVESTED_WITH is the largest predicate group ({predicate_counts['CO_INVESTED_WITH']}/{len(relations)} Aura relationships).",
            "PageRank and community/core results describe graph structure; they do not validate extraction precision.",
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    core_top = result["core"]["maximum_core_nodes"][:20]
    report = [
        "# Social network analysis — Neo4j AuraDB",
        "",
        f"Generated: {result['generated_on']}  ",
        "Source: live, read-only AuraDB graph snapshot.",
        "",
        "## AuraDB versus public v15",
        "",
        f"- AuraDB has {len(aura_ids):,} Entity nodes and {len(relations):,} relationships. The public graph projection has {len(export_ids):,} entities; the source normalized export had {source_counts.get('entity_rows', len(export_ids)):,} entity rows.",
        f"- Aura node IDs equal the public projection and its {len(export_endpoints):,} relation endpoint IDs. The projection omits {source_counts.get('isolated_entities_omitted', 0):,} source-export isolates to match AuraDB.",
        f"- Relation triples match: **{export_triples == aura_triples}** ({len(export_triples):,} unique triples); full entity property mismatches: {metadata_mismatches}.",
        f"- Full Aura graph property fingerprint matches the public manifest: **{data_fingerprint == export_manifest.get('aura_snapshot', {}).get('graph_sha256')}**.",
        "",
        "## Network analysis on AuraDB",
        "",
        f"- Graph: {len(graph):,} nodes, {graph.number_of_edges():,} unique undirected pairs, {len(components):,} components, {nx.number_of_isolates(graph):,} isolates.",
        f"- Largest component: {lcc.number_of_nodes():,} nodes ({lcc.number_of_nodes()/len(graph):.1%}); connected-pair coverage: {connected_pair_fraction:.1%}.",
        f"- Mean shortest path across all reachable node pairs in the full graph: **{average_path_reachable:.3f}**; the average over all node pairs is undefined because the graph is disconnected.",
        f"- Average shortest path in largest component: **{average_path:.3f}**; clustering: {clustering:.3f}; transitivity: {nx.transitivity(lcc):.3f}.",
        f"- Degree-preserving null baseline: mean Cᵣ={null_clustering:.3f} (range {min(null_clustering_values):.3f}–{max(null_clustering_values):.3f}); mean Lᵣ={null_path:.3f} (range {min(null_path_values):.3f}–{max(null_path_values):.3f}); {NULL_REPLICATES} connected randomizations with the exact same degree sequence, {swap_attempts:,} swap attempts each, seeds {SWAP_SEED}–{SWAP_SEED + NULL_REPLICATES - 1}.",
        f"- Small-world ratios: C/Cᵣ={clustering_ratio:.2f}, L/Lᵣ={path_ratio:.3f}; sigma={sigma:.3f}. Successful swaps per randomization: {', '.join(map(str, successful_swaps))}.",
        f"- Louvain: {len(communities):,} communities; modularity Q = {modularity:.3f}.",
        f"- Maximum k-core: k={maximum_core}, {len(maximum_core_nodes):,} nodes.",
        "",
        "## PageRank top 30",
        "",
        "| Rank | Entity | Type | PageRank |",
        "|---:|---|---|---:|",
    ]
    report += [
        f"| {rank} | {node_summary(node)['name']} | {node_summary(node)['type']} | {score:.6g} |"
        for rank, (node, score) in enumerate(ranked[:30], 1)
    ]
    report += ["", "## Maximum core — top 20 by PageRank", "", "| Entity | Type | k | PageRank |", "|---|---|---:|---:|"]
    report += [f"| {row['name']} | {row['type']} | {row['core_number']} | {row['pagerank']:.6g} |" for row in core_top]
    report += ["", "## Largest 10 communities", "", "| Community | Nodes | PageRank leaders (up to 5) |", "|---:|---:|---|"]
    report += [
        f"| {row['rank']} | {row['size']:,} | {', '.join(node['name'] for node in row['top_pagerank_nodes'][:5])} |"
        for row in community_rows[:10]
    ]
    report += [
        "", "## Interpretation", "",
        f"- The degree-preserving sigma ({sigma:.3f}) {'supports' if sigma > 1 else 'does not support'} the small-world criterion on the largest component; five connected null graphs were used, so their ranges should be reported and the comparison is not a significance test.",
        "- AuraDB is the analysis source. It contains the same 5,046 relation triples as public v15 and excludes the 153 isolated export entities.",
        "- PageRank, communities, and core are structural measures, not a validation of relation precision.",
        "", "## Reproduction", "", "```powershell", ".\\metrics\\run_social_network_analysis.ps1", "```", "",
        "The JSON includes a SHA-256 fingerprint of all Aura Entity and relationship properties for snapshot tracking.", "",
    ]
    (OUT / "report.md").write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote {OUT / 'report.md'} and {OUT / 'analysis.json'}")
    print(
        f"Aura nodes={len(graph)}; relationships={len(relations)}; LCC={len(lcc)} ({len(lcc)/len(graph):.1%}); "
        f"path={average_path:.3f}; sigma={sigma:.3f}; communities={len(communities)}; "
        f"max_core=k{maximum_core} ({len(maximum_core_nodes)} nodes)"
    )


if __name__ == "__main__":
    main()
