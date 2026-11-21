import json
from uuid import uuid4

import pytest
from app import graph_rag
from app.config import Settings
from app.main import create_app
from app.schemas import MessageCreate
from fastapi.testclient import TestClient


@pytest.fixture
def settings(tmp_path):
    return Settings(
        database_url=f"sqlite:///{(tmp_path / 'chat.db').as_posix()}", mock_delay=0, chat_mode="mock"
    )


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings)) as client:
        yield client


def thread(client):
    response = client.post("/api/threads", json={})
    assert response.status_code == 200
    return response.json()["id"]


def test_backend_title_preserves_manual_rename(client):
    identifier = thread(client)
    url = f"/api/threads/{identifier}"
    response = client.post(f"{url}/title", json={"content": "  First   question  "})
    assert response.status_code == 200
    assert response.json()["title"] == "First question"
    client.patch(url, json={"title": "Custom title"})
    assert client.post(f"{url}/title", json={"content": "Another question"}).json()["title"] == "Custom title"


def test_graph_example_uses_backend(client, monkeypatch):
    graph = {"nodes": [], "edges": [], "evidence": []}
    monkeypatch.setattr("app.routes.load_example", lambda settings: {"graph": graph, "name": "TDK Ventures"})
    response = client.post("/api/graph/example")
    assert response.status_code == 200
    assert response.json()["graph"] == graph


def events(response):
    assert response.status_code == 200
    result = []
    for block in response.text.strip().split("\n\n"):
        lines = block.splitlines()
        result.append((lines[0][7:], json.loads(lines[1][6:])))
    return result


def send(client, identifier, **kwargs):
    return client.post(
        f"/api/threads/{identifier}/messages", json={"id": "user-local-1", "content": "Ai đầu tư?", **kwargs}
    )


def test_stream_snapshot_and_idempotent_retry(client, settings):
    identifier = thread(client)
    first = events(send(client, identifier))
    assert first[0][0] == "start" and first[-1][0] == "done"
    text = "".join(data["text"] for event, data in first if event == "token")
    details = next(data for event, data in first if event == "details")
    rows = client.get(f"/api/threads/{identifier}/messages").json()
    assert len(rows) == 2
    assert rows[0]["created_at"].endswith("Z")
    assert rows[1]["content"] == text and rows[1]["status"] == "completed"
    assert rows[1]["details"] == details
    assert details["graph"]["evidence"][0]["targetId"] == details["graph"]["edges"][0]["id"]
    assert details["metadata"]["retrieval_type"] == "mock"
    assert events(send(client, identifier))[-1] == first[-1]
    assert len(client.get(f"/api/threads/{identifier}/messages").json()) == 2
    # History survives a new application instance, including details.
    with TestClient(create_app(settings)) as restarted:
        assert restarted.get(f"/api/threads/{identifier}/messages").json() == rows


def test_history_parent_and_uuid_validation(client):
    identifier = thread(client)
    send(client, identifier)
    assert send(client, identifier, content="Changed content").status_code == 409
    assert send(client, identifier, id="new", content="Next").status_code == 409
    parent = client.get(f"/api/threads/{identifier}/messages").json()[-1]["id"]
    assert send(client, identifier, id="new", content="Next", parent_id=parent).status_code == 200
    assert len(client.get(f"/api/threads/{identifier}/messages").json()) == 4
    assert client.get("/api/threads/not-a-uuid").status_code == 422
    assert client.get(f"/api/threads/{uuid4()}").status_code == 404
    assert send(client, identifier, content="  ").status_code == 422


def test_failed_response_retry_does_not_duplicate_user(client, monkeypatch):
    identifier = thread(client)
    real_answer = graph_rag.answer

    def fail(*_):
        raise RuntimeError("test failure")

    monkeypatch.setattr(graph_rag, "answer", fail)
    failed = events(send(client, identifier))
    assert failed[-1][0] == "error"
    rows = client.get(f"/api/threads/{identifier}/messages").json()
    assert rows[-1]["status"] == "failed"
    monkeypatch.setattr(graph_rag, "answer", real_answer)
    assert events(send(client, identifier))[-1][0] == "done"
    rows = client.get(f"/api/threads/{identifier}/messages").json()
    assert len(rows) == 2 and rows[-1]["status"] == "completed"


def test_threads_crud_archive_and_busy_guard(client):
    from uuid import UUID

    identifier = thread(client)
    body = {"title": "Test title"}
    assert client.patch(f"/api/threads/{identifier}", json=body).json()["title"] == body["title"]
    client.patch(f"/api/threads/{identifier}", json={"archived": True})
    assert send(client, identifier).status_code == 409
    client.patch(f"/api/threads/{identifier}", json={"archived": False})
    store = client.app.state.store
    answer, _ = store.prepare(UUID(identifier), MessageCreate(id="pending", content="Pending"))
    assert send(client, identifier).status_code == 409
    assert client.delete(f"/api/threads/{identifier}").status_code == 409
    store.finish(answer.id, "partial", {}, "failed")
    assert client.delete(f"/api/threads/{identifier}").status_code == 204
    assert client.get(f"/api/threads/{identifier}/messages").status_code == 404
    assert client.get("/api/threads").json() == []
