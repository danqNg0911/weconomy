"use client";

import { useMemo } from "react";
import {
  ExportedMessageRepository,
  useAui,
  useLocalRuntime,
  useRemoteThreadListRuntime,
  type ChatModelAdapter,
  type RemoteThreadListAdapter,
  type ThreadHistoryAdapter,
} from "@assistant-ui/react";
import {
  api,
  readEvents,
  type StoredMessage,
  type StoredThread,
} from "@/lib/chat-api";

const metadata = (thread: StoredThread) => ({
  remoteId: thread.id,
  title: thread.title,
  status: thread.archived ? ("archived" as const) : ("regular" as const),
  lastMessageAt: new Date(thread.updated_at),
});
const patch = (id: string, body: object) =>
  api(`/${id}`, { method: "PATCH", body: JSON.stringify(body) });

function useHistoryAdapters() {
  const aui = useAui();
  return useMemo(
    () => ({
      history: {
        async load() {
          const id = aui.threadListItem.getState().remoteId;
          if (!id) return { messages: [] };
          const rows = await api<StoredMessage[]>(`/${id}/messages`);
          return ExportedMessageRepository.fromArray(
            rows.map((row) => ({
              id: row.id,
              role: row.role,
              content: row.content,
              createdAt: new Date(row.created_at),
              metadata: { custom: { ...row.details, serverMessageId: row.id } },
              ...(row.role === "assistant"
                ? {
                    status:
                      row.status === "completed"
                        ? { type: "complete" as const, reason: "stop" as const }
                        : {
                            type: "incomplete" as const,
                            reason: "error" as const,
                            error: "Câu trả lời bị gián đoạn. Bấm thử lại.",
                          },
                  }
                : {}),
            })),
          );
        },
        // The backend writes both messages atomically with the streaming lifecycle.
        // Do not append a second copy from the runtime's history callbacks.
        async append() {},
      } satisfies ThreadHistoryAdapter,
    }),
    [aui],
  );
}

const threadAdapter: RemoteThreadListAdapter = {
  storeKey: "weconomy-fastapi",
  async list(params) {
    const offset = Number(params?.after || 0);
    const rows = await api<StoredThread[]>(`?limit=100&offset=${offset}`);
    return {
      threads: rows.map(metadata),
      ...(rows.length === 100 ? { nextCursor: String(offset + 100) } : {}),
    };
  },
  async initialize() {
    const thread = await api<StoredThread>("", {
      method: "POST",
      body: JSON.stringify({ id: crypto.randomUUID() }),
    });
    return { remoteId: thread.id };
  },
  async fetch(id) {
    return metadata(await api<StoredThread>(`/${id}`));
  },
  async rename(id, title) {
    await patch(id, { title });
  },
  async archive(id) {
    await patch(id, { archived: true });
  },
  async unarchive(id) {
    await patch(id, { archived: false });
  },
  async delete(id) {
    await api(`/${id}`, { method: "DELETE" });
  },
  async generateTitle(id, messages) {
    const first = messages.find((message) => message.role === "user");
    const text =
      first?.content
        .filter((part) => part.type === "text")
        .map((part) => part.text)
        .join(" ") || "New chat";
    const { title } = await api<StoredThread>(`/${id}/title`, {
      method: "POST",
      body: JSON.stringify({ content: text }),
    });
    return new ReadableStream({
      start(controller) {
        controller.enqueue({
          type: "part-start",
          path: [0],
          part: { type: "text" },
        });
        controller.enqueue({ type: "text-delta", path: [0], textDelta: title });
        controller.enqueue({ type: "part-finish", path: [0] });
        controller.close();
      },
    });
  },
  unstable_useAdapters: useHistoryAdapters,
};

function useThreadRuntime() {
  const aui = useAui();
  const model = useMemo<ChatModelAdapter>(
    () => ({
      async *run({ messages, abortSignal }) {
        const { remoteId } = await aui.threadListItem.initialize();
        const user = messages.at(-1);
        if (user?.role !== "user")
          throw new Error("Chỉ hỗ trợ câu hỏi dạng văn bản.");
        const previous = messages.at(-2);
        const parentId =
          previous?.metadata.custom?.serverMessageId || previous?.id || null;
        const content = user.content
          .filter((part) => part.type === "text")
          .map((part) => part.text)
          .join("\n");
        const response = await fetch(
          `/api/backend/threads/${remoteId}/messages`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            signal: abortSignal,
            body: JSON.stringify({ id: user.id, content, parent_id: parentId }),
          },
        );
        let text = "",
          finished = false;
        let custom: Record<string, unknown> = {};
        for await (const { event, data } of readEvents(response)) {
          if (event === "error") throw new Error(String(data.message));
          if (event === "start") custom = { serverMessageId: data.message_id };
          if (event === "token") text += String(data.text ?? "");
          if (event === "details") custom = { ...custom, ...data };
          if (event === "done") finished = true;
          yield { content: [{ type: "text", text }], metadata: { custom } };
        }
        if (!finished && !abortSignal.aborted)
          throw new Error("Stream bị gián đoạn. Bạn có thể thử lại.");
      },
    }),
    [aui],
  );
  return useLocalRuntime(model);
}

export function useBackendRuntime() {
  return useRemoteThreadListRuntime({
    adapter: threadAdapter,
    runtimeHook: useThreadRuntime,
  });
}
