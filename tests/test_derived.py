"""Synthetic investment fixtures are not news-corpus facts."""
import pytest

from weconomy.derived import shared_investment_targets


def fixture(target_type="PRODUCT"):
    entities = [{"entity_id": key, "name": key, "entity_type": kind}
                for key, kind in [("A", "ORG"), ("B", "ORG"), ("H", target_type)]]
    articles = [{"document_id": key, "text": f"{key} invested in H.", "canonical_url": f"https://example.org/{key}"}
                for key in ("A", "B")]
    claims = [{"claim_id": article["document_id"], "document_id": article["document_id"],
               "subject_id": article["document_id"], "object_id": "H", "predicate": "INVESTED_IN",
               "assertion_status": "reported", "evidence": article["text"], "evidence_start": 0,
               "evidence_end": len(article["text"])} for article in articles]
    return claims, entities, articles


@pytest.mark.parametrize("target_type", ["ORG", "PRODUCT", "PROJECT"])
def test_shared_target_preserves_target_type_and_both_proofs(target_type):
    rows = shared_investment_targets(*fixture(target_type))
    assert len(rows) == 1
    row = rows[0]
    assert (row["subject_id"], row["predicate"], row["object_id"]) == ("A", "SHARES_INVESTMENT_TARGET", "B")
    assert row["target_id"] == "H" and row["target_type"] == target_type
    assert row["supporting_claim_ids"] == ["A", "B"]
    assert row["derived"] and not row["same_round_verified"]
    assert len({item["source_url"] for item in row["supporting_evidence"]}) == 2


@pytest.mark.parametrize("change,value", [
    ("predicate", "PARTNERED_WITH"), ("assertion_status", "agreement_reported"),
    ("review_status", "rejected"), ("evidence_start", 1),
    ("evidence", "B may invest in H."), ("subject_id", "A"), ("object_id", "unknown"),
])
def test_projection_does_not_invent_missing_investments(change, value):
    claims, entities, articles = fixture()
    claims[1][change] = value
    assert not shared_investment_targets(claims, entities, articles)


def test_same_display_name_does_not_merge_distinct_targets_or_investors():
    claims, entities, articles = fixture()
    entities.append({"entity_id": "H2", "name": "H", "entity_type": "PRODUCT"})
    claims[1]["object_id"] = "H2"
    assert not shared_investment_targets(claims, entities, articles)


def test_projection_is_deterministic_and_duplicate_claims_do_not_multiply_edges():
    claims, entities, articles = fixture()
    assert shared_investment_targets(claims + claims, entities, articles) == shared_investment_targets(
        list(reversed(claims)), list(reversed(entities)), list(reversed(articles)))
