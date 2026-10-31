"""Sprint 2 baseline on an explicitly documented projection."""
import networkx as nx

from .pipeline import read_table


def analyze(run, *, small_world=False):
    graph = nx.Graph()
    entities = read_table(run, "entities")
    graph.add_nodes_from(e["entity_id"] for e in entities)
    relations = read_table(run, "relations")
    graph.add_edges_from((r["subject_id"], r["object_id"]) for r in relations)
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    largest = graph.subgraph(components[0]).copy() if components else nx.Graph()
    n = largest.number_of_nodes()
    # Ordered pairs, excluding self. Disconnected pairs excluded, with coverage made explicit.
    distances = [d for a, lengths in nx.all_pairs_shortest_path_length(largest)
                 for b, d in lengths.items() if a != b]
    result = {"projection": "undirected, unweighted, simple; all machine candidates; isolates retained",
        "nodes": graph.number_of_nodes(), "simple_edges": graph.number_of_edges(),
        "claim_edges": len(relations), "event_edges": len(read_table(run, "events")),
        "components": len(components), "largest_component_nodes": n,
        "largest_component_fraction": n / len(graph) if graph else 0,
        "reachable_ordered_pairs_lcc": len(distances), "sum_shortest_path_lcc": sum(distances),
        "average_shortest_path_lcc": sum(distances) / len(distances) if distances else None,
        "density": nx.density(graph), "average_clustering": nx.average_clustering(graph) if graph else None,
        "degree_centrality": nx.degree_centrality(graph) if graph else {},
        "pagerank": nx.pagerank(graph) if graph.number_of_edges() else {},
        "communities": [sorted(c) for c in nx.community.greedy_modularity_communities(graph)]
                       if graph.number_of_edges() else [],
        "small_world_sigma": None, "small_world_reason": "Not requested; requires connected comparison graphs"}
    if small_world:
        if n >= 10 and largest.number_of_edges() >= n and nx.average_clustering(largest) > 0:
            result["small_world_sigma"] = nx.sigma(largest, niter=5, nrand=5, seed=42)
            result["small_world_reason"] = "Pilot estimate on LCC; compare degree-preserving null, not proof"
        else:
            result["small_world_reason"] = "LCC too small/sparse or zero clustering; no valid sigma estimate"
    return result
