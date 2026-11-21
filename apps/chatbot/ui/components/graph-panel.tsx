"use client";

import { useMemo, useState } from "react";
import { useAuiState } from "@assistant-ui/react";
import { ListFilter, Network, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GraphCanvas } from "@/components/graph-canvas";
import {
  evidenceUrl,
  parseQueryGraph,
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
      className="flex h-full min-h-0 flex-col"
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
      <div className="relative flex min-h-0 flex-1 flex-col overflow-hidden">
        {graph?.nodes.length ? (
          <GraphCanvas key={`${context}:${showingSample}`} graph={graph} />
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
            className="bg-background absolute inset-y-0 right-0 z-20 flex w-[85%] max-w-sm min-w-0 flex-col border-l shadow-xl sm:w-80"
          >
            <div className="flex shrink-0 items-center justify-between px-4 py-3">
              <h3 id="evidence-heading" className="text-sm font-semibold">
                Evidence{" "}
                <span className="text-muted-foreground font-normal">
                  ({graph?.evidence.length ?? 0})
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
            <div className="min-h-0 overflow-y-auto px-4 pb-4">
              {!graph?.evidence.length ? (
                <p className="text-muted-foreground text-sm">
                  {showingSample
                    ? "Ví dụ này chỉ lấy node/edge; chưa nối dữ liệu trích dẫn."
                    : "Chưa có trích dẫn cho đồ thị này."}
                </p>
              ) : (
                <ol className="space-y-4">
                  {graph.evidence.map((item) => {
                    const target =
                      item.targetType === "node"
                        ? graph.nodes.find((n) => n.id === item.targetId)?.label
                        : graph.edges.find((e) => e.id === item.targetId)
                            ?.label;
                    const url = evidenceUrl(item.url);
                    return (
                      <li
                        key={item.id}
                        className="space-y-2 border-b pb-4 last:border-0"
                      >
                        <p className="text-muted-foreground text-xs">
                          {item.targetType === "node" ? "Node" : "Edge"} ·{" "}
                          {target}{" "}
                          <span className="font-mono">({item.targetId})</span>
                        </p>
                        <blockquote className="border-l-2 pl-3 text-sm leading-relaxed whitespace-pre-wrap">
                          {item.quote}
                        </blockquote>
                        {url && (
                          <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm break-all underline underline-offset-4"
                          >
                            {item.title || new URL(url).hostname}
                          </a>
                        )}
                      </li>
                    );
                  })}
                </ol>
              )}
            </div>
          </section>
        )}
      </div>
    </section>
  );
}
