"use client";

import { useRef, useState, type ReactNode } from "react";

export function ResizableDetailPanel({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  const panel = useRef<HTMLElement>(null);
  const dragging = useRef(false);
  const [width, setWidth] = useState(45);
  const resize = (value: number) => setWidth(Math.max(30, Math.min(70, value)));

  return (
    <aside
      ref={panel}
      id="detail-panel"
      aria-label={label}
      style={{ "--detail-width": `${width}%` } as React.CSSProperties}
      className="bg-background fixed inset-x-0 top-14 bottom-0 z-30 min-w-0 border-l md:relative md:inset-auto md:z-auto md:w-[var(--detail-width)] md:shrink-0"
    >
      <div
        role="separator"
        tabIndex={0}
        aria-label="Đổi độ rộng panel chi tiết"
        aria-orientation="vertical"
        aria-controls="detail-panel"
        aria-valuemin={30}
        aria-valuemax={70}
        aria-valuenow={Math.round(width)}
        aria-valuetext={`${Math.round(width)}%`}
        title="Kéo để đổi độ rộng; nhấp đúp để đặt lại"
        className="group absolute inset-y-0 -left-1 z-40 hidden w-2 cursor-col-resize touch-none outline-none md:block"
        onPointerDown={(event) => {
          if (event.button !== 0) return;
          event.preventDefault();
          dragging.current = true;
          event.currentTarget.setPointerCapture(event.pointerId);
        }}
        onPointerMove={(event) => {
          if (!dragging.current) return;
          const bounds = panel.current?.parentElement?.getBoundingClientRect();
          if (bounds?.width)
            resize(((bounds.right - event.clientX) / bounds.width) * 100);
        }}
        onPointerUp={() => {
          dragging.current = false;
        }}
        onPointerCancel={() => {
          dragging.current = false;
        }}
        onLostPointerCapture={() => {
          dragging.current = false;
        }}
        onDoubleClick={() => setWidth(45)}
        onKeyDown={(event) => {
          if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key))
            return;
          event.preventDefault();
          resize(
            event.key === "Home"
              ? 30
              : event.key === "End"
                ? 70
                : width + (event.key === "ArrowLeft" ? 2 : -2),
          );
        }}
      >
        <div className="bg-foreground/0 group-hover:bg-foreground/20 group-focus-visible:bg-foreground/30 absolute inset-y-0 left-[3px] w-0.5 transition-colors" />
      </div>
      {children}
    </aside>
  );
}
