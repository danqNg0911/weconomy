import pytest
from app import graph_rag, guards
from app.config import Settings
from app.llm import LLMError
from app.main import create_app
from fastapi.testclient import TestClient


class Node(dict):
    def __init__(self, identifier):
        super().__init__(name=identifier, entity_type="ORG")
        self.element_id = identifier


class Edge(dict):
    def __init__(self, identifier, source, target):
        super().__init__()
        self.element_id, self.start_node, self.end_node = identifier, source, target
        self.type = "INVESTED_IN"


def test_edge_evidence_resolves_claim_quote_and_prefers_reviewed():
    edge = Edge("r", Node("A"), Node("B"))
    edge["event_details_json"] = (
        '[{"claims":['
        '{"claim_id":"auto","evidence":"auto quote","review_status":"unreviewed"},'
        '{"claim_id":"checked","evidence":"checked quote","review_status":"manually_verified",'
        '"url":"https://example.com","title":"Source"}]}]'
    )
    evidence = graph_rag.edge_evidence(edge)
    assert evidence[0]["claimId"] == "checked"
    assert evidence[0]["quote"] == "checked quote"
    assert evidence[0]["url"] == "https://example.com"


def test_real_frontier_multi_hop_direction_and_caps():
    a, b, c, d = [Node(i) for i in "ABCD"]
    ab, cb, cd = Edge("ab", a, b), Edge("cb", c, b), Edge("cd", c, d)
    adjacency = {"A": [(ab, b)], "B": [(ab, a), (cb, c)], "C": [(cb, b), (cd, d)], "D": [(cd, c)]}

    class Transaction:
        def run(self, query, **params):
            if query == graph_rag.LINK_QUERY:
                return [{"n": a}]
            return [{"r": e, "m": n} for e, n in adjacency[params["id"]]][: params["limit"]]

    plan = graph_rag.Plan(entities=["A fund"], terms=[], relations=["INVESTED_IN"])
    settings = Settings(_env_file=None, graph_max_hops=2)
    details = graph_rag.traverse(Transaction(), settings, plan)
    assert {n["id"] for n in details["graph"]["nodes"]} == {"A", "B", "C"}
    assert details["metadata"]["hop_count"] == 2
    assert {"nodes": ["A", "B", "C"], "edges": ["ab", "cb"]} in details["metadata"]["paths"]
    assert details["graph"]["edges"][1]["source"] == "C"
    assert details["graph"]["edges"][1]["target"] == "B"
    settings.graph_max_hops = 3
    assert len(graph_rag.traverse(Transaction(), settings, plan)["graph"]["nodes"]) == 4
    settings.graph_neighbors_per_node = 1
    assert graph_rag.traverse(Transaction(), settings, plan)["metadata"]["truncated"] is True


@pytest.mark.anyio
async def test_guards_short_circuit(monkeypatch):
    calls = []

    async def classify(settings, instruction, data, schema):
        calls.append(instruction)
        return guards.Verdict(allowed=False)

    monkeypatch.setattr(guards, "structured", classify)
    assert (await guards.check(None, "cách rửa tiền", []))[0] == "safety"
    assert calls == []
    assert (await guards.check(None, "outside topic", []))[0] == "domain"
    assert len(calls) == 1
    calls.clear()

    async def classify_domain(settings, instruction, data, schema):
        calls.append(instruction)
        return guards.Verdict(allowed=False)

    monkeypatch.setattr(guards, "structured", classify_domain)
    assert (await guards.check(None, "write a game", []))[0] == "domain"
    assert len(calls) == 1


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.parametrize("blocked", [True, False])
def test_pipeline_persists_graph_or_refusal_and_replays(tmp_path, monkeypatch, blocked):
    settings = Settings(_env_file=None, chat_mode="llm", database_url=f"sqlite:///{tmp_path / 'chat.db'}")
    calls = []

    async def check(*args):
        calls.append("guards")
        return ("domain", guards.DOMAIN) if blocked else (None, None)

    async def structured(*args):
        calls.append("plan")
        return graph_rag.Plan(entities=["TDK Ventures"], terms=[], relations=[])

    snapshot = {
        "graph": {
            "nodes": [{"id": "a", "label": "TDK Ventures"}, {"id": "b", "label": "C2i"}],
            "edges": [{"id": "r", "source": "a", "target": "b", "label": "INVESTED_IN"}],
            "evidence": [],
        },
        "metadata": {"retrieval_type": "graphrag", "hop_count": 2, "paths": [], "queries": []},
    }

    def retrieve(*args):
        calls.append("retrieve")
        return snapshot

    async def stream(settings, history, instruction):
        calls.append("synthesize")
        assert "TDK Ventures" in instruction and "C2i" in instruction
        yield "TDK Ventures đầu tư vào C2i."

    monkeypatch.setattr(guards, "check", check)
    monkeypatch.setattr(guards, "structured", structured)
    monkeypatch.setattr(graph_rag, "retrieve", retrieve)
    monkeypatch.setattr("app.routes.stream_text", stream)
    with TestClient(create_app(settings)) as client:
        identifier = client.post("/api/threads", json={}).json()["id"]
        url = f"/api/threads/{identifier}/messages"
        payload = {"id": "q1", "content": "TDK Ventures đầu tư vào ai?"}
        assert "event: done" in client.post(url, json=payload).text
        rows = client.get(url).json()
        assert rows[-1]["status"] == "completed"
        if blocked:
            assert calls == ["guards"]
            assert rows[-1]["details"]["metadata"]["blocked_by"] == "domain"
            assert rows[-1]["details"]["graph"]["nodes"] == []
        else:
            assert calls == ["guards", "plan", "retrieve", "synthesize"]
            assert rows[-1]["details"] == snapshot
        before = list(calls)
        assert "event: done" in client.post(url, json=payload).text
        assert calls == before


@pytest.mark.anyio
async def test_invalid_guard_output_fails_closed(monkeypatch):
    async def stream(*args):
        yield '{"allowed":"true"}'

    monkeypatch.setattr(guards, "stream_text", stream)
    with pytest.raises(LLMError):
        await guards.structured(Settings(_env_file=None), "guard", {}, guards.Verdict)


@pytest.mark.anyio
async def test_no_matches_returns_without_synthesis(monkeypatch):
    async def check(*args):
        return None, None

    async def structured(*args):
        return graph_rag.Plan(entities=["Unknown fund"], terms=[], relations=[])

    monkeypatch.setattr(guards, "check", check)
    monkeypatch.setattr(guards, "structured", structured)
    monkeypatch.setattr(
        graph_rag,
        "retrieve",
        lambda *args: {
            "graph": {"nodes": [], "edges": [], "evidence": []},
            "metadata": {"retrieval_type": "graphrag", "hop_count": 0},
        },
    )
    text, details, instruction = await graph_rag.prepare(Settings(_env_file=None), "Unknown fund?", [])
    assert text and instruction is None
    assert details["graph"]["edges"] == []


def test_traversal_global_caps():
    nodes = [Node(str(i)) for i in range(15)]

    class Transaction:
        def run(self, query, **params):
            if query == graph_rag.LINK_QUERY:
                return [{"n": nodes[0]}]
            source = nodes[int(params["id"])]
            return [
                {"r": Edge(f"{source.element_id}-{n.element_id}", source, n), "m": n}
                for n in nodes
                if n is not source
            ][: params["limit"]]

    settings = Settings(_env_file=None, graph_max_nodes=5, graph_max_edges=5, graph_neighbors_per_node=20)
    result = graph_rag.traverse(
        Transaction(), settings, graph_rag.Plan(entities=["Fund"], terms=[], relations=[])
    )
    assert len(result["graph"]["nodes"]) <= 5
    assert len(result["graph"]["edges"]) <= 5
    assert result["metadata"]["truncated"]
