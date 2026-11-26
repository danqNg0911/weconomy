"use client";

import { useCallback, useMemo, useState } from "react";
import { useAuiState } from "@assistant-ui/react";
import { ListFilter, Network, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GraphCanvas } from "@/components/graph-canvas";
import {
  evidenceUrl,
  filterEvidence,
  parseQueryGraph,
  type GraphTarget,
  type QueryGraph,
} from "@/lib/query-graph";

export function GraphPanel({
  onClose,
  selectedGraph,
}: {
  onClose: () => void;
  selectedGraph?: { threadId: string; messageId: string } | null;
}) {
  const [evidenceOpen, setEvidenceOpen] = useState(false);
  const threadId = useAuiState((s) => s.threads.mainThreadId);
  const message = useAuiState((s) =>
    selectedGraph?.threadId === s.threads.mainThreadId
      ? s.thread.messages.find((m) => m.id === selectedGraph.messageId)
      : s.thread.messages.at(-1),
  );
  const context = `${threadId}:${message?.id ?? "empty"}`;
  const [sample, setSample] = useState<{
    context: string;
    graph: QueryGraph;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const raw =
    message?.role === "assistant" ? message.metadata.custom?.graph : undefined;
  const answerGraph = useMemo(() => parseQueryGraph(raw), [raw]);
  const showingSample = sample?.context === context;
  const graph = showingSample ? sample.graph : answerGraph;
  const [selection, setSelection] = useState<{
    graph: QueryGraph;
    evidenceId: string;
  } | null>(null);
  const selectedEvidence =
    selection?.graph === graph
      ? graph?.evidence.find((item) => item.id === selection?.evidenceId)
      : undefined;
  const [filter, setFilter] = useState<{
    graph: QueryGraph;
    target: GraphTarget;
  } | null>(null);
  const activeFilter = filter?.graph === graph ? filter?.target : undefined;
  const evidence =
    graph && activeFilter
      ? filterEvidence(graph, activeFilter)
      : (graph?.evidence ?? []);
  const nodeLabel = (id: string) =>
    graph?.nodes.find((node) => node.id === id)?.label;
  const filteredEdge =
    activeFilter?.targetType === "edge"
      ? graph?.edges.find((edge) => edge.id === activeFilter.targetId)
      : undefined;
  const filterLabel = filteredEdge
    ? `${nodeLabel(filteredEdge.source)} → ${nodeLabel(filteredEdge.target)}`
    : activeFilter && nodeLabel(activeFilter.targetId);
  const selectGraphTarget = useCallback(
    (target: GraphTarget) => {
      if (!graph) return;
      setFilter({ graph, target });
      setSelection(null);
      setEvidenceOpen(true);
    },
    [graph],
  );
  const metadata = message?.metadata.custom?.metadata;
  const evidenceStatus =
    metadata && typeof metadata === "object" && "evidence_status" in metadata
      ? metadata.evidence_status
      : undefined;
  const loadSample = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/backend/graph/example", {
        method: "POST",
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Không tải được graph.");
      const result = parseQueryGraph(data.graph);
      if (!result?.nodes.length)
        throw new Error("Không tìm thấy quan hệ quanh TDK Ventures.");
      setSample({ context, graph: result });
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Không tải được graph.",
      );
    } finally {
      setLoading(false);
    }
  };
  return (
    <section
      className="@container flex h-full min-h-0 flex-col"
      aria-labelledby="graph-heading"
    >
      <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4">
        <Network className="size-4" />
        <h2 id="graph-heading" className="flex-1 font-semibold">
          Đồ thị truy vấn
        </h2>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Hiện evidence"
          aria-expanded={evidenceOpen}
          aria-controls="graph-evidence"
          onClick={() => setEvidenceOpen(!evidenceOpen)}
          className={evidenceOpen ? "bg-accent" : ""}
        >
          <ListFilter />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Đóng đồ thị"
          onClick={onClose}
        >
          <X />
        </Button>
      </header>
      <div className="border-b px-4 py-2 text-sm">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-muted-foreground">
            {showingSample
              ? "Ví dụ AuraDB · TDK Ventures · tối đa 2 hop"
              : selectedGraph?.threadId === threadId
                ? "Đồ thị của câu trả lời đã chọn"
                : "Đồ thị của tin nhắn mới nhất"}
          </span>
          {showingSample ? (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setSample(null);
                setError("");
              }}
            >
              Đóng ví dụ
            </Button>
          ) : (
            <Button
              variant="outline"
              size="sm"
              disabled={loading}
              onClick={loadSample}
            >
              {loading ? "Đang tải…" : "Thử graph AuraDB"}
            </Button>
          )}
        </div>
        {error && (
          <p role="alert" className="text-destructive mt-2">
            {error}
          </p>
        )}
      </div>
      <div className="flex min-h-0 flex-1 flex-col overflow-hidden @md:flex-row">
        {graph?.nodes.length ? (
          <GraphCanvas
            key={`${context}:${showingSample}`}
            graph={graph}
            highlight={selectedEvidence ?? activeFilter}
            focusHighlight={Boolean(selectedEvidence)}
            onSelect={selectGraphTarget}
          />
        ) : (
          <div className="text-muted-foreground flex min-h-40 flex-1 flex-col items-center justify-center gap-3 p-8 text-center text-sm">
            <Network className="size-8 opacity-50" />
            <p>Chưa có đồ thị cho câu trả lời này.</p>
            <p>
              Đường đi truy vấn sẽ xuất hiện tại đây khi có kết quả GraphRAG.
            </p>
          </div>
        )}
        {evidenceOpen && (
          <section
            id="graph-evidence"
            aria-labelledby="evidence-heading"
            className="bg-background flex max-h-[45%] w-full shrink-0 flex-col border-t @md:max-h-none @md:w-[42%] @md:max-w-xs @md:border-t-0 @md:border-l"
          >
            <div className="flex shrink-0 items-center justify-between px-4 py-3">
              <h3 id="evidence-heading" className="text-sm font-semibold">
                Evidence{" "}
                <span
                  aria-live="polite"
                  className="text-muted-foreground font-normal"
                >
                  ({evidence.length}
                  {activeFilter ? `/${graph?.evidence.length ?? 0}` : ""})
                </span>
              </h3>
              <Button
                variant="ghost"
                size="icon-sm"
                aria-label="Đóng evidence"
                onClick={() => setEvidenceOpen(false)}
              >
                <X />
              </Button>
            </div>
            {activeFilter && (
              <div className="bg-muted mx-4 mb-3 flex shrink-0 items-center justify-between gap-2 rounded-md px-3 py-1.5 text-xs">
                <span className="min-w-0 break-words">
                  {filterLabel}
                  {filteredEdge && (
                    <span className="text-muted-foreground mt-0.5 block">
                      {filteredEdge.label}
                    </span>
                  )}
                </span>
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() => {
                    setFilter(null);
                    setSelection(null);
                  }}
                >
                  Bỏ lọc
                </Button>
              </div>
            )}
            <div className="min-h-0 overflow-y-auto px-4 pb-4">
              {!evidence.length ? (
                <p className="text-muted-foreground text-sm">
                  {activeFilter
                    ? "Chưa có trích dẫn cho mục đã chọn."
                    : showingSample
                      ? "Chưa tìm thấy trích dẫn nguồn cho dữ liệu ví dụ này."
                      : evidenceStatus === "missing_index"
                        ? "Chưa có chỉ mục dữ liệu nguồn để tra cứu claim. Cần nhập bộ Parquet/export vào backend."
                        : evidenceStatus === "partial" ||
                            evidenceStatus === "missing_source"
                          ? "Chưa tìm được đoạn trích gốc cho các cạnh này trong dữ liệu nguồn hiện có."
                          : "Chưa có trích dẫn cho đồ thị này."}
                </p>
              ) : (
                graph && (
                  <ol className="space-y-4">
                    {evidence.map((item) => {
                      const target =
                        item.targetType === "node"
                          ? graph.nodes.find((n) => n.id === item.targetId)
                              ?.label
                          : graph.edges.find((e) => e.id === item.targetId)
                              ?.label;
                      const url = evidenceUrl(item.url);
                      const selected = selectedEvidence?.id === item.id;
                      return (
                        <li
                          key={item.id}
                          className={`bg-muted/40 overflow-hidden rounded-lg border border-white ring-1 ${selected ? "ring-amber-400" : "ring-black/15 dark:ring-0"}`}
                        >
                          <button
                            type="button"
                            aria-pressed={selected}
                            onClick={() =>
                              setSelection(
                                selected
                                  ? null
                                  : { graph, evidenceId: item.id },
                              )
                            }
                            className="hover:bg-accent focus-visible:ring-ring block w-full cursor-pointer space-y-2 p-3 text-left focus-visible:ring-2 focus-visible:outline-none focus-visible:ring-inset"
                          >
                            {target && (
                              <span className="block text-xs font-semibold">
                                {target}
                              </span>
                            )}
                            <span className="block text-sm leading-relaxed whitespace-pre-wrap">
                              {item.quote}
                            </span>
                          </button>
                          {url && (
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="block px-3 pb-3 text-sm break-words italic underline underline-offset-4"
                            >
                              {item.title || new URL(url).hostname}
                            </a>
                          )}
                        </li>
                      );
                    })}
                  </ol>
                )
              )}
            </div>
          </section>
        )}
      </div>
    </section>
  );
}
