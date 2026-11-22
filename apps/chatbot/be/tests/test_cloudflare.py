import asyncio
import json
from types import SimpleNamespace

import httpx
import pytest
from app import llm
from app.config import Settings


def test_apertus_cloudflare_stream(monkeypatch):
    account = "a" * 32
    settings = Settings(
        _env_file=None,
        llm_provider="cloudflare",
        cloudflare_account_id=account,
        cloudflare_api_token="cloudflare-test-token",
        openai_api_key="old-provider-key",
        openai_api_mode="responses",
        openai_reasoning_effort="high",
    )

    def provider(request):
        assert (
            str(request.url)
            == f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/v1/chat/completions"
        )
        assert request.headers["authorization"] == "Bearer cloudflare-test-token"
        body = json.loads(request.content)
        assert body["model"] == "@cf/swiss-ai/apertus-v1.5-8b"
        assert body["stream"] is True and "messages" in body
        assert "reasoning_effort" not in body and "input" not in body
        return httpx.Response(
            200,
            text='data: {"choices":[{"delta":{"content":"OK"},"finish_reason":null}]}\n\ndata: [DONE]\n\n',
        )

    original = httpx.AsyncClient
    monkeypatch.setattr(
        llm.httpx, "AsyncClient", lambda **kwargs: original(transport=httpx.MockTransport(provider), **kwargs)
    )

    async def run():
        message = SimpleNamespace(role="user", content="Hello", status="completed", details={})
        return [chunk async for chunk in llm.stream_text(settings, [message])]

    assert asyncio.run(run()) == ["OK"]


def test_cloudflare_missing_credentials_does_not_use_previous_provider_key():
    settings = Settings(_env_file=None, llm_provider="cloudflare", openai_api_key="old-provider-key")
    assert not settings.openai_api_key.get_secret_value()

    async def run():
        return [chunk async for chunk in llm.stream_text(settings, [])]

    with pytest.raises(llm.LLMError, match="CLOUDFLARE_ACCOUNT_ID"):
        asyncio.run(run())


def test_cloudflare_gated_model_has_safe_specific_message(monkeypatch):
    settings = Settings(
        _env_file=None,
        llm_provider="cloudflare",
        cloudflare_account_id="a" * 32,
        cloudflare_api_token="test-token",
    )
    original = httpx.AsyncClient
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            403, json={"errors": [{"code": 5018, "message": "private provider response not for clients"}]}
        )
    )
    monkeypatch.setattr(llm.httpx, "AsyncClient", lambda **kwargs: original(transport=transport, **kwargs))

    async def run():
        return [chunk async for chunk in llm.stream_text(settings, [])]

    with pytest.raises(llm.LLMError, match="403/5018") as caught:
        asyncio.run(run())
    assert "private provider response" not in str(caught.value)
