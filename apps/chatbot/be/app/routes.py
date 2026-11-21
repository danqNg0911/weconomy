import asyncio
import json
import logging
from uuid import UUID

import anyio
from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool

from . import graph_rag
from .graph_example import load_example
from .llm import LLMError, stream_text
from .schemas import MessageCreate, MessageOut, ThreadCreate, ThreadOut, ThreadPatch, ThreadTitle

router = APIRouter()


def sse(event, data):
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.get("/health", tags=["threads"])
def health(request: Request):
    settings = request.app.state.settings
    return {"status": "ok", "chat_mode": settings.chat_mode}


@router.post("/api/threads", response_model=ThreadOut, tags=["threads"])
def create_thread(payload: ThreadCreate, request: Request):
    return request.app.state.store.create_thread(payload)


@router.post("/api/graph/example", tags=["message"])
def graph_example(request: Request):
    return load_example(request.app.state.settings)


@router.post("/api/threads/{identifier}/title", response_model=ThreadOut, tags=["threads"])
def title(identifier: UUID, payload: ThreadTitle, request: Request):
    return request.app.state.store.generate_title(identifier, payload.content)


@router.get("/api/threads", response_model=list[ThreadOut], tags=["threads"])
def list_threads(request: Request, limit: int = Query(100, ge=1, le=200), offset: int = Query(0, ge=0)):
    return request.app.state.store.list_threads(limit, offset)


@router.get("/api/threads/{identifier}", response_model=ThreadOut, tags=["threads"])
def get_thread(identifier: UUID, request: Request):
    return request.app.state.store.get_thread(identifier)


@router.patch("/api/threads/{identifier}", response_model=ThreadOut, tags=["threads"])
def patch_thread(identifier: UUID, payload: ThreadPatch, request: Request):
    return request.app.state.store.patch_thread(identifier, payload)


@router.delete("/api/threads/{identifier}", status_code=204, tags=["threads"])
def delete_thread(identifier: UUID, request: Request):
    request.app.state.store.delete_thread(identifier)
    return Response(status_code=204)


@router.get("/api/threads/{identifier}/messages", response_model=list[MessageOut], tags=["message"])
def history(identifier: UUID, request: Request):
    return request.app.state.store.messages(identifier)


@router.post("/api/threads/{identifier}/messages", tags=["message"])
async def send(identifier: UUID, payload: MessageCreate, request: Request):
    settings = request.app.state.settings
    store = request.app.state.store
    answer, replay = await run_in_threadpool(store.prepare, identifier, payload)

    async def stream():
        content, details, saved = "", {}, replay
        try:
            # Finish before the store's five-minute stale-pending recovery window.
            async with asyncio.timeout(240):
                yield sse("start", {"message_id": str(answer.id)})
                if replay:
                    content, details = answer.content, answer.details
                    yield sse("token", {"text": content})
                else:
                    messages = await run_in_threadpool(store.messages, identifier)
                    if settings.chat_mode == "mock":
                        text, details = await run_in_threadpool(
                            graph_rag.answer, payload.content, messages[:-1]
                        )
                        for index in range(0, len(text), 24):
                            await asyncio.sleep(settings.mock_delay)
                            chunk = text[index : index + 24]
                            content += chunk
                            yield sse("token", {"text": chunk})
                    else:
                        text, details, instruction = await graph_rag.prepare(
                            settings, payload.content, messages[:-1]
                        )
                        if text is not None:
                            content = text
                            yield sse("token", {"text": content})
                        else:
                            async for chunk in stream_text(settings, messages[:-1], instruction):
                                content += chunk
                                yield sse("token", {"text": chunk})
                    await run_in_threadpool(store.finish, answer.id, content, details, "completed")
                    saved = True
                yield sse("details", details)
                yield sse("done", {"message_id": str(answer.id)})
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logging.error("Chat stream failed (%s)", type(exc).__name__)
            yield sse(
                "error",
                {
                    "message": str(exc)
                    if isinstance(exc, LLMError)
                    else "Không tạo được câu trả lời. Bạn có thể thử lại."
                },
            )
        finally:
            if not saved:
                # Preserve partial output even if Stop/disconnect cancels the response.
                with anyio.CancelScope(shield=True):
                    await run_in_threadpool(store.finish, answer.id, content, details, "failed")

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
