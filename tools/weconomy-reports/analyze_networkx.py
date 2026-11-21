#!/usr/bin/env python3
"""Read-only AuraDB -> NetworkX graph analysis for a Weconomy report.

Preserves all Entity nodes, collapses multi-edges for analysis, keeps directed
G and simple undirected H to distinguish analytical projections. Saves only
aggregated graph metrics; does NOT modify Neo4j.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import statistics

import networkx as nx
from neo4j import GraphDatabase, READ_ACCESS


def load_neo4j_env():
    """Load Neo4j settings from the nearest .env without overriding the shell."""
    base = Path(__file__).resolve().parent
    env_file = next((folder / ".env" for folder in (base, *base.parents)
                     if (folder / ".env").is_file()), None)
    if env_file is None:
        return
    keys = {"NEO4J_URI", "NEO4J_USER", "NEO4J_USERNAME", "NEO4J_PASSWORD", "NEO4J_DATABASE"}
    for line in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.removeprefix("export ").split("=", 1)
        if key.strip() in keys:
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def top(values, names, k=25):
    return [{"entity_id": node, "name": names.get(node, node), "score": round(float(score), 8)}
            for node, score in sorted(values.items(), key=lambda t: t[1], reverse=True)[:k]]


def main():
    parser = argparse.ArgumentParser(description="Graph structural metrics from Neo4j AuraDB")
    parser.add_argument("--output", default="reports")
    parser.add_argument("--advanced", action="store_true", help="Clustering, communities, shortest paths, betweenness")
    args = parser.parse_args()
    load_neo4j_env()
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER") or os.getenv("NEO4J_USERNAME") or "neo4j"
    password = os.getenv("NEO4J_PASSWORD")
    if not uri or not password:
        parser.error("NEO4J_URI and NEO4J_PASSWORD are required")

    directed = nx.DiGraph()
    undirected = nx.Graph()
    names = {}
    edge_types = Counter()
    raw_edges = 0
    raw_self_loops = 0
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session(default_access_mode=READ_ACCESS) as session:
            for rec in session.run("MATCH (n:Entity) RETURN elementId(n) AS id, "
                                   "coalesce(n.name,n.canonical_name,n.entity_id) AS name"):
                ident = rec["id"]
                names[ident] = str(rec["name"] or ident)
                directed.add_node(ident)
                undirected.add_node(ident)
            for rec in session.run("MATCH (a:Entity)-[r]->(b:Entity) "
                                   "RETURN elementId(a) AS src, elementId(b) AS dst, type(r) AS predicate"):
                a, b = rec["src"], rec["dst"]
                raw_edges += 1
                edge_types[rec["predicate"]] += 1
                raw_self_loops += (a == b)
                if a != b:
                    directed.add_edge(a, b)
                    undirected.add_edge(a, b)

    n = directed.number_of_nodes()
    weak = sorted(nx.weakly_connected_components(directed), key=len, reverse=True)
    strong = sorted(nx.strongly_connected_components(directed), key=len, reverse=True)
    comps = sorted(nx.connected_components(undirected), key=len, reverse=True)
    deg = dict(directed.degree())
    indeg = dict(directed.in_degree())
    outdeg = dict(directed.out_degree())
    pagerank = nx.pagerank(directed, alpha=.85) if n else {}
    hist = Counter(deg.values())
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "notes": ["Raw Neo4j edges may be directed multi-edges with event IDs.",
                  "Directed NetworkX graph collapses same ordered endpoint pair and omits self-loops.",
                  "Undirected NetworkX graph drops direction, parallel edges and self-loops.",
                  "All nodes are retained, including isolated nodes."],
        "raw_entity_nodes": n, "raw_entity_edges": raw_edges,
        "observed_predicates": dict(edge_types),
        "raw_self_loops": raw_self_loops,
        "directed_simple_edges": directed.number_of_edges(),
        "undirected_simple_edges": undirected.number_of_edges(),
        "directed_simple_density": nx.density(directed),
        "undirected_simple_density": nx.density(undirected),
        "isolated_nodes": len(list(nx.isolates(undirected))),
        "weak_components": len(weak), "weak_largest_component_size": len(weak[0]) if weak else 0,
        "strong_components": len(strong), "strong_largest_component_size": len(strong[0]) if strong else 0,
        "undirected_components": len(comps), "largest_component_size": len(comps[0]) if comps else 0,
        "component_sizes_top25": [len(c) for c in comps[:25]],
        "reciprocity_directed_simple": nx.reciprocity(directed) if directed.number_of_edges() else None,
        "degree_histogram": dict(sorted(hist.items())),
        "average_total_degree_directed_simple": statistics.mean(deg.values()) if deg else 0,
        "top_degree": top(deg, names), "top_in_degree": top(indeg, names),
        "top_out_degree": top(outdeg, names), "top_pagerank": top(pagerank, names),
    }
    if args.advanced and n:
        print("Computing clustering, triangles, communities, path lengths and approximate betweenness...", flush=True)
        summary["average_clustering_undirected"] = nx.average_clustering(undirected)
        summary["transitivity_undirected"] = nx.transitivity(undirected)
        summary["triangles_undirected"] = sum(nx.triangles(undirected).values()) // 3
        # Standard greedy modularity on simple undirected graph, may take time for large data.
        communities = (list(nx.community.greedy_modularity_communities(undirected))
                       if undirected.number_of_edges() else [{node} for node in undirected.nodes()])
        summary["communities"] = len(communities)
        summary["community_sizes_top25"] = sorted((len(c) for c in communities), reverse=True)[:25]
        summary["community_modularity"] = nx.community.modularity(undirected, communities) if undirected.number_of_edges() else 0
        if comps:
            largest = undirected.subgraph(comps[0])
            summary["average_shortest_path_largest_component"] = (
                nx.average_shortest_path_length(largest) if largest.number_of_nodes() > 1 else 0)
        k = min(100,n)
        bet = nx.betweenness_centrality(undirected, k=k if k<n else None, seed=42)
        summary["betweenness_approx_sample_k"] = k
        summary["top_betweenness_approx"] = top(bet, names)

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "networkx_metrics.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    sections = ["# Weconomy NetworkX metrics", "",
                "**Note:** Metric values for NetworkX simple graph should not be described as Neo4j raw multi-graph metrics.", ""]
    for key, value in summary.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            sections.append(f"- **{key}:** {value}")
    for name in ["top_degree", "top_pagerank", "top_betweenness_approx", "component_sizes_top25", "community_sizes_top25"]:
        if name in summary:
            sections.extend([f"\n## {name}", "```json", json.dumps(summary[name], indent=2, ensure_ascii=False), "```"])
    (output / "networkx_metrics.md").write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Report: {(output / 'networkx_metrics.json').resolve()}")


if __name__ == "__main__":
    main()
