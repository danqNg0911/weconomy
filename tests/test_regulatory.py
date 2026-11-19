"""Synthetic sentences exercise legal-event semantics, not legal advice or corpus facts."""
from pathlib import Path

import pytest

from weconomy.entity_quality import government_aliases
from weconomy.nlp import NLP, extract_relations, supported_relation
from weconomy.pipeline import load_config


def mentions(text, names):
    return sorted([{"start": text.index(name), "end": text.index(name) + len(name), "surface": name,
                    "entity": {"entity_id": name, "entity_type": kind}}
                   for name, kind in names], key=lambda row: row["start"])


@pytest.mark.parametrize("text,predicate,expected", [
    ("SEC is investigating venture firm Acme.", "INVESTIGATES", True),
    ("SEC was also investigating whether Acme lied to investors.", "INVESTIGATES", True),
    ("Acme was still under investigation by SEC.", "INVESTIGATES", True),
    ("SEC has closed its investigation into electric vehicle startup Acme.", "CLOSED_INVESTIGATION_INTO", True),
    ("SEC ended a probe into bankrupt EV startup Acme.", "CLOSED_INVESTIGATION_INTO", True),
    ("SEC is not investigating Acme.", "INVESTIGATES", False),
    ("If SEC is investigating Acme, it could matter.", "INVESTIGATES", False),
    ("SEC may investigate Acme.", "INVESTIGATES", False),
    ("SEC is investigating Acme.", "SUED", False),
    ("SEC opened an antitrust investigation against Acme.", "ANTITRUST_ACTION_AGAINST", False),
    ("SEC brought an antitrust case against Acme.", "ANTITRUST_ACTION_AGAINST", True),
    ("SEC has closed its investigation into Acme.", "INVESTIGATES", False),
    ("SEC recommends closing its investigation into Acme.", "CLOSED_INVESTIGATION_INTO", False),
])
def test_investigation_and_closure_are_distinct_named_events(text, predicate, expected):
    found = mentions(text, [("SEC", "GOV"), ("Acme", "ORG")])
    assert supported_relation(text, found, "en", predicate, "SEC", "Acme") is expected
    if expected:
        rows = [r for r in extract_relations(text, found, "en") if r["predicate"] == predicate]
        assert len(rows) == 1
        if "was " in text:
            assert rows[0]["assertion_status"] == "historical_reported"


@pytest.mark.parametrize("text,expected", [
    ("Microsoft licensed technology from GitHub.", True),
    ("Microsoft paid GitHub $2.4 billion to license its technology.", True),
    ("Microsoft agreed to pay GitHub $2.4 billion to license its technology.", False),
    ("Microsoft reportedly paid GitHub $2.4 billion to license its technology.", False),
    ("Microsoft paid GitHub $2.4 billion for consulting.", False),
    ("A subsidiary of Microsoft paid GitHub $2.4 billion to license its technology.", False),
])
def test_technology_license_is_not_a_whole_company_acquisition(text, expected):
    found = mentions(text, [("Microsoft", "ORG"), ("GitHub", "ORG")])
    assert supported_relation(text, found, "en", "LICENSED_TECH_FROM", "Microsoft", "GitHub") is expected
    assert not supported_relation(text, found, "en", "ACQUIRED", "Microsoft", "GitHub")


def test_government_alias_requires_document_identity_and_jurisdiction():
    assert not government_aliases("Securities and Exchange Commission discussed Acme.")
    assert not government_aliases("The Trump administration discussed SEC.")
    aliases = government_aliases("The Securities and Exchange Commission sent Wells Notices to Acme.")
    assert aliases["sec"]["entity_type"] == "GOV"
    assert aliases["sec"]["name"].startswith("United States ")
    mixed = government_aliases("United States Securities and Exchange Commission and the Southeastern Conference (SEC).")
    assert "sec" not in mixed


@pytest.mark.parametrize("text,predicate", [
    ("SEC đang điều tra Acme.", "INVESTIGATES"),
    ("SEC đã kết thúc cuộc điều tra đối với Acme.", "CLOSED_INVESTIGATION_INTO"),
    ("SEC chưa điều tra Acme.", None),
])
def test_vietnamese_government_actions_need_a_positive_explicit_predicate(text, predicate):
    found = mentions(text, [("SEC", "GOV"), ("Acme", "ORG")])
    rows = extract_relations(text, found, "vi")
    assert [row["predicate"] for row in rows] == ([predicate] if predicate else [])


def test_vietnamese_technology_license_direction():
    text = "Acme đã nhận quyền sử dụng công nghệ từ Globex."
    found = mentions(text, [("Acme", "ORG"), ("Globex", "ORG")])
    assert supported_relation(text, found, "vi", "LICENSED_TECH_FROM", "Acme", "Globex")
    assert not supported_relation(text, found, "vi", "ACQUIRED", "Acme", "Globex")


def test_government_type_is_resolved_before_new_sentence_claims_and_reset_between_documents():
    config = load_config(Path(__file__).resolve().parents[1] / "config/pipeline.yaml")
    engine = NLP(config)
    text = "SEC was investigating whether Microsoft lied."
    engine.begin_document("United States Securities and Exchange Commission. " + text)
    found = engine.mentions(text, "en")
    assert found[0]["entity"]["entity_type"] == "GOV"
    claims = engine.relations(text, found, "en")
    assert len(claims) == 1 and claims[0]["predicate"] == "INVESTIGATES"
    assert claims[0]["assertion_status"] == "historical_reported"
    engine.begin_document("A college team in the Southeastern Conference plays tonight.")
    assert not engine._document_governments
