"use client";

import { useEffect, useState } from "react";
import { PanelRight } from "lucide-react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useBackendRuntime } from "@/hooks/use-backend-runtime";
import { Thread } from "@/components/thread.aui";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { ThreadListSidebar } from "@/components/threadlist-sidebar.aui";
import { Button } from "@/components/ui/button";
import { GraphPanel } from "@/components/graph-panel";
import { ResizableDetailPanel } from "@/components/resizable-detail-panel";
import type { GraphSelection } from "@/lib/query-graph";

export const Assistant = () => {
  const [panel, setPanel] = useState<"graph" | null>(null);
  const [selectedGraph, setSelectedGraph] = useState<GraphSelection | null>(
    null,
  );
  useEffect(() => {
    const close = (event: KeyboardEvent) => {
      if (event.key === "Escape" && !document.getElementById("graph-evidence"))
        setPanel(null);
    };
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, []);
  const runtime = useBackendRuntime();

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <SidebarProvider>
        <div className="flex h-dvh w-full overflow-hidden">
          <ThreadListSidebar />
          <SidebarInset className="min-h-0 min-w-0 overflow-hidden">
            <div className="flex h-full min-h-0 min-w-0">
              <div className="flex min-h-0 min-w-0 flex-1 flex-col">
                <header className="flex h-14 shrink-0 items-center gap-3 px-4">
                  <SidebarTrigger />
                  <span className="flex-1 text-lg font-semibold">Weconomy</span>
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label="Hiện đồ thị truy vấn"
                    aria-expanded={panel === "graph"}
                    aria-controls="detail-panel"
                    onClick={() => {
                      setSelectedGraph(null);
                      setPanel((p) =>
                        selectedGraph
                          ? "graph"
                          : p === "graph"
                            ? null
                            : "graph",
                      );
                    }}
                    className={panel === "graph" ? "bg-accent" : ""}
                  >
                    <PanelRight />
                  </Button>
                </header>
                <div className="min-h-0 flex-1 overflow-hidden">
                  <Thread
                    linearHistory
                    onViewGraph={(threadId, messageId, evidenceId) => {
                      setSelectedGraph({ threadId, messageId, evidenceId });
                      setPanel("graph");
                    }}
                  />
                </div>
              </div>
              {panel && (
                <ResizableDetailPanel label="Chi tiết đồ thị">
                  <GraphPanel
                    selectedGraph={selectedGraph}
                    onClose={() => setPanel(null)}
                  />
                </ResizableDetailPanel>
              )}
            </div>
          </SidebarInset>
        </div>
      </SidebarProvider>
    </AssistantRuntimeProvider>
  );
};
