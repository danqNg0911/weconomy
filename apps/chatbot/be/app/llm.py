"""OpenAI-compatible streaming shared by guards, planning and answer generation."""

import asyncio
import json

import httpx

from .config import Settings


class LLMError(Exception):
    """Safe message to show to the client; never include provider response bodies."""


def request_body(settings: Settings, history, instruction: str | None = None, max_tokens: int | None = None):
    messages = [{"role": "system", "content": instruction or settings.llm_system_prompt}]
    turns = [
        {"role": item.role, "content": item.content if item is history[-1] else item.content[:2000]}
        for item in history
        if item.status == "completed"
        and item.content
        and item.details.get("metadata", {}).get("retrieval_type") not in {"mock", "guard"}
    ]
    messages.extend(turns[-settings.llm_history_messages :])
    body = {"model": settings.openai_model, "stream": True}
    budget = max_tokens or settings.llm_max_output_tokens
    if settings.openai_api_mode == "chat":
        body["max_tokens"] = budget
        body["messages"] = messages
        if settings.openai_reasoning_effort:
            body["reasoning_effort"] = settings.openai_reasoning_effort
    else:
        body["max_output_tokens"] = budget
        body["input"] = messages
        reasoning = {}
        if settings.openai_reasoning_effort:
            reasoning["effort"] = settings.openai_reasoning_effort
        if settings.openai_reasoning_summary:
            reasoning["summary"] = settings.openai_reasoning_summary
        if reasoning:
            body["reasoning"] = reasoning
    return body


async def stream_text(
    settings: Settings, history, instruction: str | None = None, max_tokens: int | None = None
):
    if settings.llm_provider == "cloudflare" and (
        not settings.cloudflare_account_id or not settings.cloudflare_api_token.get_secret_value()
    ):
        raise LLMError(
            "Điền CLOUDFLARE_ACCOUNT_ID và CLOUDFLARE_API_TOKEN trong backend .env, rồi khởi động lại backend."
        )
    if not settings.openai_model or not settings.openai_api_key.get_secret_value():
        raise LLMError("Thiếu OPENAI_MODEL hoặc OPENAI_API_KEY trong cấu hình backend.")
    endpoint = "chat/completions" if settings.openai_api_mode == "chat" else "responses"
    base = (settings.openai_base_url or "https://api.openai.com/v1").rstrip("/")
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key.get_secret_value()}",
        "Accept": "text/event-stream",
    }
    finished, received = False, False
    try:
        async with asyncio.timeout(180), httpx.AsyncClient(timeout=httpx.Timeout(120, connect=15)) as client:
            async with client.stream(
                "POST",
                f"{base}/{endpoint}",
                headers=headers,
                json=request_body(settings, history, instruction, max_tokens),
            ) as response:
                if not response.is_success:
                    if response.status_code == 403 and settings.llm_provider == "cloudflare":
                        try:
                            data = json.loads(await response.aread())
                            codes = {
                                item.get("code") for item in data.get("errors", []) if isinstance(item, dict)
                            }
                        except (ValueError, TypeError, AttributeError):
                            codes = set()
                        if codes & {5018, 3041}:
                            raise LLMError(
                                "Tài khoản Cloudflare chưa được cấp quyền dùng model này (HTTP 403/5018). Cần đăng ký quyền truy cập trên trang model trước khi chat."
                            )
                    if response.status_code == 429:
                        raise LLMError(
                            "Provider đang quá tải hoặc đã giới hạn tần suất/quota (HTTP 429). Hãy chờ rồi thử lại."
                        )
                    raise LLMError(
                        f"LLM trả HTTP {response.status_code}. Kiểm tra API key, Base URL và tên model."
                    )
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        finished = True
                        break
                    if not data:
                        continue
                    event = json.loads(data)
                    if event.get("error") or event.get("type") in {
                        "error",
                        "response.failed",
                        "response.incomplete",
                    }:
                        raise LLMError("LLM báo lỗi hoặc chưa hoàn tất câu trả lời. Hãy thử lại.")
                    chunk, truncated = "", False
                    if settings.openai_api_mode == "chat":
                        for choice in event.get("choices", []):
                            delta = choice.get("delta", {})
                            value = delta.get("content") or delta.get("refusal") or ""
                            if isinstance(value, str):
                                chunk += value
                            if choice.get("finish_reason") is not None:
                                finished = True
                            truncated |= choice.get("finish_reason") == "length"
                    elif event.get("type") in {"response.output_text.delta", "response.refusal.delta"}:
                        chunk = event.get("delta", "")
                    elif event.get("type") == "response.completed":
                        finished = True
                    if chunk:
                        received = True
                        yield chunk
                    if truncated:
                        raise LLMError(
                            "LLM đã đạt giới hạn token; phản hồi chưa hoàn tất. Hãy rút gọn câu hỏi hoặc tăng ngân sách token."
                        )
    except (httpx.RequestError, TimeoutError) as exc:
        raise LLMError("Không kết nối được LLM hoặc đã hết thời gian chờ. Kiểm tra router/endpoint.") from exc
    if not finished or not received:
        raise LLMError("LLM trả stream rỗng hoặc bị gián đoạn. Hãy thử lại.")
