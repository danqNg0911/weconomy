"use client";

import { useEffect, useRef, useState } from "react";
import type { NVL } from "@neo4j-nvl/base";
import { Maximize, Minus, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { QueryGraph } from "@/lib/query-graph";

const colors = ["#5b8def", "#a78bfa", "#34b399", "#f0ab58", "#f472b6"];

/** Render only the backend snapshot, without browser database credentials. */
export function GraphCanvas({ graph }: { graph: QueryGraph }) {
  const container = useRef<HTMLDivElement>(null);
  const instance = useRef<NVL | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let disposed = false;
    let cleanup = () => {};
    setError("");
    async function mount() {
      const [
        { NVL },
        { ZoomInteraction, PanInteraction, DragNodeInteraction },
      ] = await Promise.all([
        import("@neo4j-nvl/base"),
        import("@neo4j-nvl/interaction-handlers"),
      ]);
      if (disposed || !container.current) return;
      const types = [...new Set(graph.nodes.map((n) => n.type || "Entity"))];
      const label = (text: string) => {
        const element = document.createElement("span");
        element.textContent = text;
        element.className =
          "text-foreground pointer-events-none whitespace-nowrap text-xs";
        return element;
      };
      const nodes = graph.nodes.map((node) => {
        const html = label(node.label);
        html.dataset.nodeId = node.id;
        html.style.display = "block";
        html.style.transform = "translateY(28px)";
        return {
          id: node.id,
          size: 20,
          color: colors[types.indexOf(node.type || "Entity") % colors.length],
          html,
        };
      });
      const rels = graph.edges.map((edge) => ({
        id: edge.id,
        from: edge.source,
        to: edge.target,
        type: edge.label,
        captionHtml: label(edge.label),
        color: "#9298a2",
      }));
      const nvl = new NVL(
        container.current,
        nodes,
        rels,
        {
          layout: "forceDirected",
          renderer: "canvas",
          disableWebGL: true,
          disableWebWorkers: true,
          disableTelemetry: true,
          maxZoom: 4,
        },
        { onLayoutDone: () => nvl.fit(nodes.map((n) => n.id), { maxZoom: 1.5 }) },
      );
      instance.current = nvl;
      const handlers = [
        new ZoomInteraction(nvl),
        new PanInteraction(nvl),
        new DragNodeInteraction(nvl),
      ];
      let resizeTimer: ReturnType<typeof setTimeout>;
      const observer = new ResizeObserver(() => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(
          () => nvl.fit(nodes.map((n) => n.id), { maxZoom: 1.5 }),
          120,
        );
      });
      observer.observe(container.current);
      cleanup = () => {
        clearTimeout(resizeTimer);
        observer.disconnect();
        handlers.forEach((handler) => handler.destroy());
        instance.current = null;
        nvl.destroy();
      };
    }
    mount().catch(() => {
      if (!disposed)
        setError("Không khởi tạo được đồ thị. Hãy đóng và mở lại panel.");
    });
    return () => {
      disposed = true;
      cleanup();
    };
  }, [graph]);
  const zoom = (factor: number) => {
    const nvl = instance.current;
    if (nvl) nvl.setZoom(nvl.getScale() * factor);
  };
  return (
    <div
      className="relative h-full min-h-0 flex-1"
      aria-label="Đồ thị truy vấn Neo4j"
    >
      <div
        ref={container}
        className="absolute inset-0"
        data-graph-renderer="neo4j-nvl"
      />
      {error && (
        <p role="alert" className="relative p-4 text-sm">
          {error}
        </p>
      )}
      <div className="bg-background/90 absolute bottom-4 left-4 flex gap-1 rounded-xl border p-1 shadow-sm">
        <Button
          variant="ghost"
          size="icon"
          aria-label="Phóng to"
          onClick={() => zoom(1.2)}
        >
          <Plus />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Thu nhỏ"
          onClick={() => zoom(1 / 1.2)}
        >
          <Minus />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Vừa khung đồ thị"
          onClick={() =>
            instance.current?.fit(graph.nodes.map((n) => n.id), { maxZoom: 1.5 })
          }
        >
          <Maximize />
        </Button>
      </div>
    </div>
  );
}
