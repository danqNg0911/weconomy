import json

import httpx
import pytest
from app import llm
from app.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def isolate_provider_transport(monkeypatch):
    # These tests exercise the provider transport, not guard/retrieval models.
    async def prepare(settings, question, history):
        return (
            None,
            {
                "graph": {"nodes": [], "edges": [], "evidence": []},
                "metadata": {"retrieval_type": "llm", "model": settings.openai_model},
            },
            settings.llm_system_prompt,
        )

    monkeypatch.setattr("app.graph_rag.prepare", prepare)


@pytest.mark.parametrize("mode", ["chat", "responses"])
def test_llm_stream_persists_real_answer_shape(tmp_path, monkeypatch, mode):
    settings = Settings(
        _env_file=None,
        chat_mode="llm",
        database_url=f"sqlite:///{(tmp_path / 'llm.db').as_posix()}",
        openai_api_key="test-key",
        openai_base_url="https://router.invalid/v1",
        openai_model="configured-model",
        openai_api_mode=mode,
    )
    requests = []

    def provider(request):
        requests.append(request)
        body = json.loads(request.content)
        assert body["model"] == "configured-model" and body["stream"] is True
        assert request.headers["authorization"] == "Bearer test-key"
        turns = body["messages" if mode == "chat" else "input"]
        assert turns[-1] == {"role": "user", "content": "Hello"}
        if mode == "chat":
            data = [
                {"choices": [{"delta": {"content": "Xin chào"}, "finish_reason": None}]},
                {"choices": [{"delta": {}, "finish_reason": "stop"}]},
            ]
        else:
            data = [
                {"type": "response.output_text.delta", "delta": "Xin chào"},
                {"type": "response.completed"},
            ]
        return httpx.Response(
            200, text="".join(f"data: {json.dumps(event)}\n\n" for event in data) + "data: [DONE]\n\n"
        )

    real_client = httpx.AsyncClient
    monkeypatch.setattr(
        llm.httpx,
        "AsyncClient",
        lambda **kwargs: real_client(transport=httpx.MockTransport(provider), **kwargs),
    )
    with TestClient(create_app(settings)) as client:
        identifier = client.post("/api/threads", json={}).json()["id"]
        response = client.post(f"/api/threads/{identifier}/messages", json={"id": "user", "content": "Hello"})
        assert "event: done" in response.text
        rows = client.get(f"/api/threads/{identifier}/messages").json()
        assert rows[-1]["content"] == "Xin chào" and rows[-1]["status"] == "completed"
        assert rows[-1]["details"]["metadata"] == {"retrieval_type": "llm", "model": "configured-model"}
        assert rows[-1]["details"]["graph"] == {"nodes": [], "edges": [], "evidence": []}
        # Completed replay reads DB, without another provider call.
        client.post(f"/api/threads/{identifier}/messages", json={"id": "user", "content": "Hello"})
        assert len(requests) == 1


@pytest.mark.parametrize(
    "status,body",
    [
        (401, "secret provider error body"),
        (200, 'data: {"choices":[{"delta":{"content":"partial"}}]}\n\n'),
    ],
)
def test_provider_failure_and_truncated_stream_are_not_completed(tmp_path, monkeypatch, status, body):
    settings = Settings(
        _env_file=None,
        chat_mode="llm",
        database_url=f"sqlite:///{(tmp_path / 'error.db').as_posix()}",
        openai_api_key="test-key",
        openai_model="test",
        openai_api_mode="chat",
    )
    real_client = httpx.AsyncClient
    transport = httpx.MockTransport(lambda request: httpx.Response(status, text=body))
    monkeypatch.setattr(llm.httpx, "AsyncClient", lambda **kwargs: real_client(transport=transport, **kwargs))
    with TestClient(create_app(settings)) as client:
        identifier = client.post("/api/threads", json={}).json()["id"]
        response = client.post(f"/api/threads/{identifier}/messages", json={"id": "user", "content": "Hello"})
        assert "event: error" in response.text and "event: done" not in response.text
        assert "secret provider error body" not in response.text
        assert "test-key" not in response.text
        row = client.get(f"/api/threads/{identifier}/messages").json()[-1]
        assert row["status"] == "failed"
        if status == 200:
            assert row["content"] == "partial"
