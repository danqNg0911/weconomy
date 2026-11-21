export type StoredThread = {
  id: string;
  title: string;
  archived: boolean;
  updated_at: string;
};
export type StoredMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  details: Record<string, unknown>;
  status: "pending" | "completed" | "failed";
  created_at: string;
};

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/backend/threads${path}`, {
    ...init,
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : `Chat API error (${response.status})`,
    );
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

/** Incremental SSE parser: handles UTF-8 split across network chunks. */
export async function* readEvents(response: Response) {
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(
      typeof body?.detail === "string"
        ? body.detail
        : "Không gửi được tin nhắn.",
    );
  }
  if (!response.body) throw new Error("Empty response stream");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      const { done, value } = await reader.read();
      buffer += decoder.decode(value, { stream: !done });
      buffer = buffer.replace(/\r\n/g, "\n");
      let end: number;
      while ((end = buffer.indexOf("\n\n")) !== -1) {
        const lines = buffer.slice(0, end).split("\n");
        buffer = buffer.slice(end + 2);
        const event = lines
          .find((line) => line.startsWith("event:"))
          ?.slice(6)
          .trim();
        const data = lines
          .filter((line) => line.startsWith("data:"))
          .map((line) => line.slice(5).trimStart())
          .join("\n");
        if (event && data)
          yield { event, data: JSON.parse(data) as Record<string, unknown> };
      }
      if (done) break;
    }
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}
