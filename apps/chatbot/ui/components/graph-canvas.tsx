"use client";

import { useEffect, useRef, useState } from "react";
import type { NVL } from "@neo4j-nvl/base";
import { Maximize, Minus, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { GraphTarget, QueryGraph } from "@/lib/query-graph";

const colors = ["#5b8def", "#a78bfa", "#34b399", "#f0ab58", "#f472b6"];
const focusColor = "#fbbf24";

/** Render only the backend snapshot, without browser database credentials. */
export function GraphCanvas({
  graph,
  highlight,
  focusHighlight,
  onSelect,
}: {
  graph: QueryGraph;
  highlight?: GraphTarget;
  focusHighlight: boolean;
  onSelect: (target: GraphTarget) => void;
}) {
  const container = useRef<HTMLDivElement>(null);
  const instance = useRef<NVL | null>(null);
  const focusNodes = useRef<string[]>([]);
  const [renderer, setRenderer] = useState<NVL | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let disposed = false;
    let cleanup = () => {};
    setError("");
    async function mount() {
      const [
        { NVL },
        {
          ClickInteraction,
          ZoomInteraction,
          PanInteraction,
          DragNodeInteraction,
        },
      ] = await Promise.all([
        import("@neo4j-nvl/base"),
        import("@neo4j-nvl/interaction-handlers"),
      ]);
      if (disposed || !container.current) return;
      const types = [...new Set(graph.nodes.map((n) => n.type || "Entity"))];
      const label = (text: string, target: GraphTarget) => {
        const element = document.createElement("button");
        element.type = "button";
        element.textContent = text;
        element.className =
          "text-foreground pointer-events-auto cursor-pointer whitespace-nowrap text-xs hover:underline focus-visible:underline";
        element.setAttribute("aria-label", `Lọc trích dẫn cho ${text}`);
        element.onclick = (event) => {
          event.stopPropagation();
          onSelect(target);
        };
        return element;
      };
      const nodes = graph.nodes.map((node) => {
        const html = label(node.label, {
          targetType: "node",
          targetId: node.id,
        });
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
        captionHtml: label(edge.label, {
          targetType: "edge",
          targetId: edge.id,
        }),
        color: "#9298a2",
      }));
      const fitGraph = () =>
        nvl.fit(
          focusNodes.current.length
            ? focusNodes.current
            : nodes.map((node) => node.id),
          { maxZoom: 1.5 },
        );
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
        { onLayoutDone: fitGraph },
      );
      instance.current = nvl;
      setRenderer(nvl);
      const click = new ClickInteraction(nvl);
      const selectHit = (
        targetType: GraphTarget["targetType"],
        hit: unknown,
      ) => {
        if (
          hit &&
          typeof hit === "object" &&
          "id" in hit &&
          typeof hit.id === "string"
        ) {
          onSelect({ targetType, targetId: hit.id });
        }
      };
      click.updateCallback("onNodeClick", (node) => selectHit("node", node));
      click.updateCallback("onRelationshipClick", (edge) =>
        selectHit("edge", edge),
      );
      const handlers = [
        click,
        new ZoomInteraction(nvl),
        new PanInteraction(nvl),
        new DragNodeInteraction(nvl),
      ];
      let resizeTimer: ReturnType<typeof setTimeout>;
      const observer = new ResizeObserver(() => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(fitGraph, 120);
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
  }, [graph, onSelect]);
  useEffect(() => {
    if (!renderer || renderer !== instance.current) return;
    const edge =
      highlight?.targetType === "edge"
        ? graph.edges.find((item) => item.id === highlight.targetId)
        : undefined;
    const highlightedNodes = edge
      ? [edge.source, edge.target]
      : highlight?.targetType === "node"
        ? [highlight.targetId]
        : [];
    focusNodes.current = focusHighlight ? highlightedNodes : [];
    const types = [
      ...new Set(graph.nodes.map((node) => node.type || "Entity")),
    ];
    renderer.updateElementsInGraph(
      graph.nodes.map((node) => {
        const focused = highlightedNodes.includes(node.id);
        return {
          id: node.id,
          size: focused ? 25 : 20,
          color: focused
            ? focusColor
            : colors[types.indexOf(node.type || "Entity") % colors.length],
        };
      }),
      graph.edges.map((item) => ({
        id: item.id,
        color: item.id === edge?.id ? focusColor : "#9298a2",
        width: item.id === edge?.id ? 4 : 1,
      })),
    );
    if (focusNodes.current.length)
      renderer.fit(focusNodes.current, { maxZoom: 1.5 });
  }, [graph, renderer, highlight, focusHighlight]);
  const zoom = (factor: number) => {
    const nvl = instance.current;
    if (nvl) nvl.setZoom(nvl.getScale() * factor);
  };
  return (
    <div
      className="relative h-full min-h-0 min-w-0 flex-1"
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
            instance.current?.fit(
              graph.nodes.map((n) => n.id),
              { maxZoom: 1.5 },
            )
          }
        >
          <Maximize />
        </Button>
      </div>
    </div>
  );
}
