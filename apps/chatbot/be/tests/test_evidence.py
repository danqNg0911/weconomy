import json

from app.config import Settings
from app.evidence import build_index, edge_claim_ids, enrich


def test_indexed_evidence_joins_claim_to_article_and_preserves_quote(tmp_path):
    (tmp_path / "claims.jsonl").write_text(
        json.dumps(
            {
                "claim_id": "c1",
                "document_id": "d1",
                "evidence": "Exact original quotation.",
                "review_status": "manually_verified",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "articles.jsonl").write_text(
        json.dumps(
            {
                "document_id": "d1",
                "title": "Article",
                "url": "https://example.com/source",
                "source_id": "news",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "audit").mkdir()
    (tmp_path / "audit" / "claims.jsonl").write_text(
        json.dumps({"claim_id": "c1", "document_id": "d1", "evidence": "Discarded revision."}) + "\n",
        encoding="utf-8",
    )
    index = tmp_path / "index.sqlite3"
    assert build_index([tmp_path], index) == {"claims": 1, "documents": 1}
    settings = Settings(_env_file=None, evidence_index_path=str(index))
    details = {
        "graph": {"edges": [{"id": "edge", "claim_ids": ["c1", "missing"]}], "evidence": []},
        "metadata": {},
    }
    result = enrich(settings, details)
    item = result["graph"]["evidence"][0]
    assert item["targetId"] == "edge" and item["quote"] == "Exact original quotation."
    assert item["url"] == "https://example.com/source" and item["claimId"] == "c1"
    assert result["metadata"]["evidence_status"] == "partial"
    assert result["metadata"]["evidence_claims_missing"] == 1
    assert edge_claim_ids({"event_details_json": '[{"claim_ids":["c1","c1"]}]'}) == ["c1"]


def test_missing_index_does_not_fabricate_evidence(tmp_path):
    settings = Settings(_env_file=None, evidence_index_path=str(tmp_path / "missing.db"))
    details = {"graph": {"edges": [{"id": "edge", "claim_ids": ["c1"]}], "evidence": []}, "metadata": {}}
    assert enrich(settings, details)["metadata"]["evidence_status"] == "missing_index"
    assert details["graph"]["evidence"] == []


def test_claim_without_source_article_is_not_citable(tmp_path):
    (tmp_path / "claims.jsonl").write_text(
        json.dumps({"claim_id": "c1", "document_id": "missing", "evidence": "A stored quotation."}) + "\n",
        encoding="utf-8",
    )
    index = tmp_path / "index.sqlite3"
    build_index([tmp_path], index)
    settings = Settings(_env_file=None, evidence_index_path=str(index))
    details = {"graph": {"edges": [{"id": "edge", "claim_ids": ["c1"]}], "evidence": []}, "metadata": {}}

    assert enrich(settings, details)["metadata"]["evidence_status"] == "partial"
    assert details["graph"]["evidence"] == []
