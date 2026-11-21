import { isAllowedRequestContext } from "../../request-context";

export const runtime = "nodejs";

async function proxy(
  req: Request,
  context: { params: Promise<{ path: string[] }> },
) {
  if (!isAllowedRequestContext(req))
    return Response.json(
      { detail: "Cross-origin request refused" },
      { status: 403 },
    );
  const { path } = await context.params;
  if (
    path[0] !== "threads" &&
    !(path.length === 2 && path[0] === "graph" && path[1] === "example")
  )
    return new Response(null, { status: 404 });
  const base = (
    process.env.CHAT_BACKEND_URL || "http://127.0.0.1:8000"
  ).replace(/\/$/, "");
  try {
    const upstream = await fetch(
      `${base}/api/${path.map(encodeURIComponent).join("/")}${new URL(req.url).search}`,
      {
        method: req.method,
        headers: { "Content-Type": "application/json" },
        body:
          req.method === "GET" || req.method === "DELETE"
            ? undefined
            : await req.arrayBuffer(),
        cache: "no-store",
        signal: req.signal,
      },
    );
    return new Response(upstream.body, {
      status: upstream.status,
      headers: {
        "Content-Type":
          upstream.headers.get("content-type") || "application/json",
        "Cache-Control": "no-store",
        "X-Accel-Buffering": "no",
      },
    });
  } catch {
    return Response.json(
      { detail: "Không kết nối được FastAPI. Hãy chạy backend ở cổng 8000." },
      { status: 502 },
    );
  }
}

export { proxy as GET, proxy as POST, proxy as PATCH, proxy as DELETE };
