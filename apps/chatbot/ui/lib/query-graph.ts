/** Neo4j query subgraph normalized by the backend (never database credentials). */
export type GraphNode = { id: string; label: string; type?: string };
export type GraphEdge = {
  id: string;
  source: string;
  target: string;
  label: string;
};
export type GraphEvidence = {
  id: string;
  targetType: "node" | "edge";
  targetId: string;
  quote: string;
  url?: string;
  title?: string;
  claimId?: string;
  source?: string;
  reviewStatus?: string;
  assertionStatus?: string;
  trigger?: string;
};
export type GraphTarget = Pick<GraphEvidence, "targetType" | "targetId">;
export type GraphSelection = {
  threadId: string;
  messageId: string;
  evidenceId?: string;
};
export type QueryGraph = {
  nodes: GraphNode[];
  edges: GraphEdge[];
  evidence: GraphEvidence[];
};

export function filterEvidence(graph: QueryGraph, target: GraphTarget) {
  if (target.targetType === "edge") {
    return graph.evidence.filter(
      (item) => item.targetType === "edge" && item.targetId === target.targetId,
    );
  }
  const incidentEdges = new Set(
    graph.edges
      .filter(
        (edge) =>
          edge.source === target.targetId || edge.target === target.targetId,
      )
      .map((edge) => edge.id),
  );
  return graph.evidence.filter((item) =>
    item.targetType === "edge"
      ? incidentEdges.has(item.targetId)
      : item.targetId === target.targetId,
  );
}

const record = (value: unknown): value is Record<string, unknown> =>
  value !== null && typeof value === "object" && !Array.isArray(value);
const string = (value: unknown): value is string => typeof value === "string";

/** Partial streamed or malformed metadata must not break the chat UI. */
export function parseQueryGraph(value: unknown): QueryGraph | null {
  if (
    !record(value) ||
    !Array.isArray(value.nodes) ||
    !Array.isArray(value.edges)
  )
    return null;
  const nodes = value.nodes.filter(
    (n): n is GraphNode => record(n) && string(n.id) && string(n.label),
  );
  const ids = new Set(nodes.map((n) => n.id));
  const edges = value.edges.filter(
    (e): e is GraphEdge =>
      record(e) &&
      string(e.id) &&
      string(e.source) &&
      string(e.target) &&
      string(e.label) &&
      ids.has(e.source) &&
      ids.has(e.target),
  );
  const edgeIds = new Set(edges.map((e) => e.id));
  const evidence = Array.isArray(value.evidence)
    ? value.evidence.filter(
        (e): e is GraphEvidence =>
          record(e) &&
          string(e.id) &&
          string(e.targetId) &&
          string(e.quote) &&
          (e.targetType === "node"
            ? ids.has(e.targetId)
            : e.targetType === "edge" && edgeIds.has(e.targetId)) &&
          (e.url === undefined || string(e.url)) &&
          (e.title === undefined || string(e.title)) &&
          (e.claimId === undefined || string(e.claimId)) &&
          (e.source === undefined || string(e.source)) &&
          (e.reviewStatus === undefined || string(e.reviewStatus)) &&
          (e.assertionStatus === undefined || string(e.assertionStatus)) &&
          (e.trigger === undefined || string(e.trigger)),
      )
    : [];
  return {
    nodes: [...new Map(nodes.map((n) => [n.id, n])).values()],
    edges: [...new Map(edges.map((e) => [e.id, e])).values()],
    evidence,
  };
}

export function evidenceUrl(value?: string): string | undefined {
  try {
    const url = new URL(value ?? "");
    return url.protocol === "https:" || url.protocol === "http:"
      ? url.href
      : undefined;
  } catch {
    return undefined;
  }
}

export function resolveCitation(
  graph: QueryGraph | null,
  metadata: unknown,
  href: string,
) {
  if (!graph) return undefined;
  const index = /^\/evidence\/([1-9]\d*)$/.exec(href);
  if (index) {
    const ids = record(metadata) ? metadata.citation_ids : undefined;
    const id = Array.isArray(ids) ? ids[Number(index[1]) - 1] : undefined;
    const item = graph.evidence.find((evidence) => evidence.id === id);
    return item && { item, label: `Nguồn ${index[1]}` };
  }
  const url = evidenceUrl(href);
  const item = url
    ? graph.evidence.find((evidence) => evidenceUrl(evidence.url) === url)
    : undefined;
  return item && url
    ? { item, label: new URL(url).hostname.replace(/^www\./, "") }
    : undefined;
}
