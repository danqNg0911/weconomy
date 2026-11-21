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
};
export type QueryGraph = {
  nodes: GraphNode[];
  edges: GraphEdge[];
  evidence: GraphEvidence[];
};

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
          (e.title === undefined || string(e.title)),
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
