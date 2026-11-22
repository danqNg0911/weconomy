import json
from copy import deepcopy

import httpx
import pytest
from app import graph_rag, llm
from app.config import Settings
from app.graph_selection import select_graph
from app.main import create_app
from fastapi.testclient import TestClient
from pydantic import ValidationError


def graph():
    return {
        "graph": {
            "nodes": [{"id": n, "label": n} for n in "ABCD"],
            "edges": [
                {"id": "ac", "source": "A", "target": "C", "label": "INVESTED_IN"},
                {"id": "bc", "source": "B", "target": "C", "label": "INVESTED_IN"},
                {"id": "ad", "source": "A", "target": "D", "label": "INVESTED_IN"},
            ],
            "evidence": [
                {
                    "id": "quote",
                    "targetType": "edge",
                    "targetId": "ac",
                    "quote": "Source quotation",
                    "url": "https://example.com",
                }
            ],
        },
        "metadata": {"retrieval_type": "graphrag", "seed_ids": ["A", "B"], "paths": [], "truncated": False},
    }


def test_multi_hop_selection_and_direction():
    for kind in ("common_investments", "connection"):
        selected = select_graph(graph(), kind, ["A", "B"], 3)
        assert {e["id"] for e in selected["graph"]["edges"]} == {"ac", "bc"}
        assert selected["metadata"]["paths"] == [{"nodes": ["A", "C", "B"], "edges": ["ac", "bc"]}]
    data = graph()
    data["metadata"]["seed_ids"] = ["C"]
    assert len(select_graph(deepcopy(data), "investors", ["C"], 3)["graph"]["edges"]) == 2
    assert select_graph(deepcopy(data), "investments", ["C"], 3)["graph"]["edges"] == []
    assert select_graph(graph(), "connection", ["A", "B"], 1)["graph"]["edges"] == []


@pytest.mark.parametrize("ambiguous", [False, True])
def test_workflow_budgets_clarification_and_saved_snapshot(tmp_path, monkeypatch, ambiguous):
    settings = Settings(
        _env_file=None,
        llm_provider="cloudflare",
        cloudflare_account_id="a" * 32,
        cloudflare_api_token="test-token",
        database_url=f"sqlite:///{tmp_path / 'workflow.db'}",
    )
    calls, retrievals = [], []

    def provider(request):
        body = json.loads(request.content)
        calls.append(body)
        assert body["model"] == "@cf/swiss-ai/apertus-v1.5-8b"
        if len(calls) == 1:
            text = '{"allowed":true}'
            assert body["max_tokens"] == 64
        elif len(calls) == 2:
            text = json.dumps(
                {
                    "entities": ["A", "B"],
                    "terms": [],
                    "relations": ["INVESTED_IN"],
                    "intent": "ambiguous" if ambiguous else "common_investments",
                    "clarification": "Which direction?" if ambiguous else "",
                }
            )
            assert body["max_tokens"] == 512
        else:
            assert body["max_tokens"] == 1024
            assert "Source quotation" in body["messages"][0]["content"]
            text = "A and B invest in C."
        return httpx.Response(
            200,
            text="data: "
            + json.dumps({"choices": [{"delta": {"content": text}, "finish_reason": None}]})
            + "\n\ndata: [DONE]\n\n",
        )

    original = httpx.AsyncClient
    monkeypatch.setattr(
        llm.httpx, "AsyncClient", lambda **kwargs: original(transport=httpx.MockTransport(provider), **kwargs)
    )

    def retrieve(settings, plan):
        retrievals.append(plan)
        result = select_graph(graph(), plan.intent, plan.entities, 3)
        result["metadata"]["plan"] = plan.model_dump(mode="json")
        return result

    monkeypatch.setattr(graph_rag, "retrieve", retrieve)
    with TestClient(create_app(settings)) as client:
        identifier = client.post("/api/threads", json={}).json()["id"]
        url = f"/api/threads/{identifier}/messages"
        payload = {"id": "question", "content": "Which companies do A and B both invest in?"}
        response = client.post(url, json=payload)
        assert "event: done" in response.text
        row = client.get(url).json()[-1]
        assert row["status"] == "completed"
        assert len(calls) == (2 if ambiguous else 3)
        assert len(retrievals) == (0 if ambiguous else 1)
        if not ambiguous:
            assert row["details"]["metadata"]["hop_count"] == 2
            assert len(row["details"]["graph"]["evidence"]) == 1
        client.post(url, json=payload)
        assert len(calls) == (2 if ambiguous else 3)


def test_plan_rejects_executable_relation_and_excessive_hops():
    for extra in [{"relations": ["MATCH (n) DELETE n"]}, {"max_hops": 20}, {"intent": "run_cypher"}]:
        values = {"entities": ["A"], "terms": [], "relations": []} | extra
        with pytest.raises(ValidationError):
            graph_rag.Plan(**values)


def test_date_filter_keeps_only_matching_event_claims():
    from datetime import date

    from test_graph_rag import Edge, Node

    raw = Edge("r", Node("A"), Node("B"))
    raw["event_details_json"] = json.dumps(
        [
            {"event_date": "2020-01-01", "claim_ids": ["old"]},
            {"event_date": "2025-05-01", "claim_ids": ["recent"]},
        ]
    )
    plan = graph_rag.Plan(entities=["A"], terms=[], relations=[], date_from=date(2025, 1, 1))
    result = graph_rag.dated_edge(raw, plan)
    assert result["claim_ids"] == ["recent"]
    assert result["date"] == "2025-05-01"
    plan.date_from = date(2026, 1, 1)
    assert graph_rag.dated_edge(raw, plan) is None
