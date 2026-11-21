"use client";

import {
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type PointerEvent,
} from "react";
import { Maximize, Minus, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { QueryGraph } from "@/lib/query-graph";

type Point = { x: number; y: number };
const colors = ["#5b8def", "#a78bfa", "#34b399", "#f0ab58", "#f472b6"];

/** Small query subgraphs only: SVG keeps labels crisp and needs no graph dependency. */
export function GraphCanvas({ graph }: { graph: QueryGraph }) {
  const markerId = useId().replaceAll(":", "");
  const svg = useRef<SVGSVGElement>(null);
  const drag = useRef<{
    pointerId: number;
    nodeId?: string;
    point: Point;
  } | null>(null);
  const [view, setView] = useState({ x: 0, y: 0, scale: 1 });
  const [positions, setPositions] = useState<Record<string, Point>>({});
  const [size, setSize] = useState({ width: 900, height: 600 });
  useEffect(() => {
    const element = svg.current;
    if (!element) return;
    const observer = new ResizeObserver(([entry]) => {
      if (entry.contentRect.width && entry.contentRect.height) {
        setSize({
          width: entry.contentRect.width,
          height: entry.contentRect.height,
        });
      }
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  const initial = useMemo(
    () =>
      new Map(
        graph.nodes.map((node, index) => {
          const angle =
            (2 * Math.PI * index) / graph.nodes.length - Math.PI / 2;
          return [
            node.id,
            {
              x:
                size.width / 2 +
                (graph.nodes.length === 1
                  ? 0
                  : size.width * 0.3 * Math.cos(angle)),
              y:
                size.height / 2 +
                (graph.nodes.length === 1
                  ? 0
                  : Math.max(0, size.height / 2 - 90) * Math.sin(angle)),
            },
          ];
        }),
      ),
    [graph.nodes, size],
  );
  const point = (id: string) => positions[id] ?? initial.get(id)!;
  const zoom = (factor: number) =>
    setView((v) => {
      const scale = Math.min(4, Math.max(0.25, v.scale * factor));
      const ratio = scale / v.scale;
      return {
        x: size.width / 2 - (size.width / 2 - v.x) * ratio,
        y: size.height / 2 - (size.height / 2 - v.y) * ratio,
        scale,
      };
    });
  const localPoint = (event: PointerEvent<SVGSVGElement>) => {
    const matrix = svg.current?.getScreenCTM()?.inverse();
    return matrix
      ? new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix)
      : { x: 0, y: 0 };
  };
  const start = (event: PointerEvent<SVGSVGElement>) => {
    if (event.button !== 0) return;
    const nodeId =
      (event.target as Element)
        .closest("[data-node-id]")
        ?.getAttribute("data-node-id") ?? undefined;
    drag.current = {
      pointerId: event.pointerId,
      nodeId,
      point: localPoint(event),
    };
    event.currentTarget.setPointerCapture(event.pointerId);
  };
  const move = (event: PointerEvent<SVGSVGElement>) => {
    const active = drag.current;
    if (!active || active.pointerId !== event.pointerId) return;
    const next = localPoint(event);
    const dx = next.x - active.point.x;
    const dy = next.y - active.point.y;
    if (active.nodeId) {
      const id = active.nodeId;
      const previous = point(id);
      setPositions((p) => ({
        ...p,
        [id]: {
          x: previous.x + dx / view.scale,
          y: previous.y + dy / view.scale,
        },
      }));
    } else setView((v) => ({ ...v, x: v.x + dx, y: v.y + dy }));
    active.point = next;
  };
  return (
    <div className="relative min-h-0 flex-1 overflow-hidden">
      <svg
        ref={svg}
        viewBox={`0 0 ${size.width} ${size.height}`}
        className="h-full w-full cursor-grab touch-none select-none active:cursor-grabbing"
        aria-label="Đồ thị truy vấn. Kéo để di chuyển; dùng nút cộng, trừ để phóng to, thu nhỏ."
        onPointerDown={start}
        onPointerMove={move}
        onPointerUp={() => {
          drag.current = null;
        }}
        onPointerCancel={() => {
          drag.current = null;
        }}
        onLostPointerCapture={() => {
          drag.current = null;
        }}
        onWheel={(event) => zoom(event.deltaY < 0 ? 1.1 : 1 / 1.1)}
      >
        <defs>
          <marker
            id={markerId}
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="7"
            markerHeight="7"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
          </marker>
        </defs>
        <g transform={`translate(${view.x} ${view.y}) scale(${view.scale})`}>
          {graph.edges.map((edge) => {
            const source = point(edge.source),
              target = point(edge.target);
            const distance =
              Math.hypot(target.x - source.x, target.y - source.y) || 1;
            const dx = ((target.x - source.x) / distance) * 25,
              dy = ((target.y - source.y) / distance) * 25;
            return (
              <g key={edge.id} className="text-muted-foreground">
                {edge.source === edge.target ? (
                  <path
                    d={`M ${source.x - 16} ${source.y - 16} c -65 -90 97 -90 32 0`}
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    markerEnd={`url(#${markerId})`}
                  />
                ) : (
                  <line
                    x1={source.x + dx}
                    y1={source.y + dy}
                    x2={target.x - dx}
                    y2={target.y - dy}
                    stroke="currentColor"
                    strokeWidth="1.5"
                    markerEnd={`url(#${markerId})`}
                  />
                )}
                <text
                  x={(source.x + target.x) / 2}
                  y={
                    (source.y + target.y) / 2 -
                    (edge.source === edge.target ? 75 : 9)
                  }
                  textAnchor="middle"
                  className="fill-muted-foreground stroke-background text-[13px] [paint-order:stroke]"
                  strokeWidth="5"
                  strokeLinejoin="round"
                >
                  {edge.label}
                </text>
              </g>
            );
          })}
          {graph.nodes.map((node, index) => {
            const p = point(node.id);
            return (
              <g
                key={node.id}
                data-node-id={node.id}
                transform={`translate(${p.x} ${p.y})`}
              >
                <circle
                  r="22"
                  fill={colors[index % colors.length]}
                  className="stroke-background"
                  strokeWidth="3"
                />
                <text
                  y="44"
                  textAnchor="middle"
                  className="fill-foreground stroke-background text-sm [paint-order:stroke]"
                  strokeWidth="5"
                  strokeLinejoin="round"
                >
                  {node.label.length > 36
                    ? `${node.label.slice(0, 33)}…`
                    : node.label}
                </text>
                <title>{node.label}</title>
              </g>
            );
          })}
        </g>
      </svg>
      <div className="bg-background absolute bottom-4 left-4 flex items-center gap-1 rounded-xl border p-1 shadow-sm">
        <Button
          variant="ghost"
          size="icon"
          aria-label="Phóng to"
          onClick={() => zoom(1.25)}
        >
          <Plus />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Thu nhỏ"
          onClick={() => zoom(0.8)}
        >
          <Minus />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Đặt lại khung nhìn"
          onClick={() => {
            setView({ x: 0, y: 0, scale: 1 });
            setPositions({});
          }}
        >
          <Maximize />
        </Button>
      </div>
    </div>
  );
}
