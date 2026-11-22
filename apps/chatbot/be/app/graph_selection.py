"""Select bounded, directed facts and actual connecting paths."""

from collections import deque


def select_graph(details, kind, entities, max_hops, max_edges=20):
    """Select directed investment facts or shortest connecting paths, not all neighbors."""
    graph, meta = details["graph"], details["metadata"]
    seeds = meta["seed_ids"]
    edges = graph["edges"]
    chosen, paths = set(), []
    investment = [e for e in edges if e["label"] == "INVESTED_IN"]
    if kind == "common_investments" and len(seeds) >= 2 and len(entities) >= 2 and max_hops >= 2:
        portfolios = [{e["target"] for e in investment if e["source"] == seed} for seed in seeds]
        shared = set.intersection(*portfolios)
        eligible = {e["id"] for e in investment if e["source"] in seeds and e["target"] in shared}
        for target in sorted(shared):
            group = {e["id"] for e in investment if e["source"] in seeds and e["target"] == target}
            if len(chosen | group) > max_edges:
                meta["truncated"] = True
                continue
            chosen.update(group)
            pair = [
                next(e for e in investment if e["source"] == seed and e["target"] == target)
                for seed in seeds[:2]
            ]
            paths.append({"nodes": [seeds[0], target, seeds[1]], "edges": [e["id"] for e in pair]})
        meta["truncated"] |= chosen != eligible
    elif kind in {"investors", "investments"} and len(entities) == 1 and len(seeds) == 1:
        direction = "target" if kind == "investors" else "source"
        chosen = {e["id"] for e in investment if e[direction] == seeds[0]}
    elif kind == "connection" and len(seeds) >= 2 and len(entities) >= 2:
        adjacency = {}
        for e in edges:
            adjacency.setdefault(e["source"], []).append((e["target"], e["id"]))
            adjacency.setdefault(e["target"], []).append((e["source"], e["id"]))
        for index, source in enumerate(seeds):
            for target in seeds[index + 1 :]:
                queue, visited = deque([(source, [source], [])]), {source}
                while queue:
                    current, ns, es = queue.popleft()
                    if current == target:
                        if len(chosen | set(es)) <= max_edges:
                            chosen.update(es)
                            paths.append({"nodes": ns, "edges": es})
                        else:
                            meta["truncated"] = True
                        break
                    if len(es) >= max_hops:
                        continue
                    for neighbor, edge_id in adjacency.get(current, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, ns + [neighbor], es + [edge_id]))
    elif kind == "neighborhood":
        chosen = {e["id"] for e in edges if e["source"] in seeds or e["target"] in seeds}
    selected = [e for e in edges if e["id"] in chosen][:max_edges]
    ids = {e["id"] for e in selected}
    node_ids = set(seeds) | {e[key] for e in selected for key in ("source", "target")}
    graph["nodes"] = [n for n in graph["nodes"] if n["id"] in node_ids]
    graph["edges"] = selected
    graph["evidence"] = [e for e in graph["evidence"] if e["targetId"] in ids]
    meta["paths"] = [p for p in paths if set(p["edges"]) <= ids] or [
        {"nodes": [e["source"], e["target"]], "edges": [e["id"]]} for e in selected
    ]
    meta["truncated"] |= len(chosen) > len(selected)
    meta["hop_count"] = max((len(p["edges"]) for p in meta["paths"]), default=0)
    meta["selection"] = kind
    return details
