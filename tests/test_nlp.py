"""Artificial sentences here are software fixtures, never corpus news."""
from pathlib import Path

import pytest

from weconomy.nlp import (
    NLP,
    document_person_aliases,
    extract_relations,
    normalize,
    route,
    sentences,
)
from weconomy.pipeline import load_config
from weconomy.schema import stable_id

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def nlp():
    return NLP(load_config(ROOT / "config/pipeline.yaml"))


@pytest.mark.parametrize("text,lang,predicate", [
    ("Microsoft acquired GitHub.", "en", "ACQUIRED"),
    ("Microsoft invested in GitHub.", "en", "INVESTED_IN"),
    ("Microsoft merged with GitHub.", "en", "MERGED_WITH"),
    ("Microsoft sued GitHub.", "en", "SUED"),
    ("Microsoft partnered with GitHub.", "en", "PARTNERED_WITH"),
    ("Microsoft supplies chips to GitHub.", "en", "SUPPLIES_TO"),
    ("Bill Gates is the CEO of Microsoft.", "en", "CEO_OF"),
    ("Bill Gates founded Microsoft.", "en", "FOUNDED"),
    ("GitHub is a subsidiary of Microsoft.", "en", "SUBSIDIARY_OF"),
    ("Microsoft owns a stake in GitHub.", "en", "OWNS_STAKE_IN"),
    ("Bill Gates is a board member of Microsoft.", "en", "BOARD_MEMBER_OF"),
    ("Microsoft signed a contract with GitHub.", "en", "CONTRACTED_WITH"),
    ("Microsoft awarded a contract to GitHub.", "en", "AWARDED_CONTRACT_TO"),
    ("United States filed an antitrust action against Microsoft.", "en", "ANTITRUST_ACTION_AGAINST"),
    ("United States sanctioned Microsoft.", "en", "SANCTIONED"),
    ("Microsoft disrupted the supply to GitHub.", "en", "DISRUPTED_SUPPLY_TO"),
    ("Microsoft spun off from GitHub.", "en", "SPUN_OFF_FROM"),
    ("Microsoft đã mua lại GitHub.", "vi", "ACQUIRED"),
    ("Microsoft đã đầu tư vào GitHub.", "vi", "INVESTED_IN"),
    ("Bill Gates thành lập Microsoft.", "vi", "FOUNDED"),
    ("Microsoft nắm giữ cổ phần tại GitHub.", "vi", "OWNS_STAKE_IN"),
    ("Bill Gates là thành viên hội đồng quản trị của Microsoft.", "vi", "BOARD_MEMBER_OF"),
    ("Microsoft ký hợp đồng với GitHub.", "vi", "CONTRACTED_WITH"),
    ("Microsoft trao hợp đồng cho GitHub.", "vi", "AWARDED_CONTRACT_TO"),
    ("United States khởi kiện chống độc quyền nhằm vào Microsoft.", "vi", "ANTITRUST_ACTION_AGAINST"),
    ("United States áp đặt trừng phạt đối với Microsoft.", "vi", "SANCTIONED"),
    ("Microsoft làm gián đoạn nguồn cung cho GitHub.", "vi", "DISRUPTED_SUPPLY_TO"),
    ("Microsoft tách ra khỏi GitHub.", "vi", "SPUN_OFF_FROM"),
])
def test_direct_rules(nlp, text, lang, predicate):
    found = extract_relations(text, nlp.mentions(text, lang), lang)
    assert len(found) == 1
    assert found[0]["predicate"] == predicate
    assert found[0]["subject_id"] != found[0]["object_id"]


def test_vietnamese_partnered_with_rule(nlp):
    text = "Microsoft k\u00fd k\u1ebft h\u1ee3p t\u00e1c v\u1edbi Vingroup."
    found = extract_relations(text, nlp.mentions(text, "vi"), "vi")
    assert len(found) == 1 and found[0]["predicate"] == "PARTNERED_WITH"


def test_antitrust_rule_rejects_non_government_subject(nlp):
    text = "Microsoft filed an antitrust action against GitHub."
    assert not extract_relations(text, nlp.mentions(text, "en"), "en")


def test_vietnamese_nhien_lieu_does_not_trigger_uncertainty_filter(nlp):
    text = "Microsoft mua lại GitHub trong bối cảnh thiếu hụt nhiên liệu."
    found = extract_relations(text, nlp.mentions(text, "vi"), "vi")
    assert len(found) == 1 and found[0]["predicate"] == "ACQUIRED"


@pytest.mark.parametrize("text,lang", [
    ("Microsoft did not acquire GitHub.", "en"),
    ("If Microsoft acquired GitHub, costs would rise.", "en"),
    ("Microsoft reportedly acquired GitHub.", "en"),
    ('"Microsoft acquired GitHub," the rumour said.', "en"),
    ("Microsoft and GitHub made announcements.", "en"),
    ("Microsoft plans to acquire GitHub.", "en"),
    ("Microsoft acquired shares in GitHub.", "en"),
    ("Microsoft acquired GitHub’s assets.", "en"),
    ("Microsoft acquired GitHub and Apple.", "en"),
    ("Microsoft chưa mua lại GitHub.", "vi"),
    ("Nếu Microsoft mua lại GitHub, họ sẽ thay đổi.", "vi"),
    ("Liệu Microsoft mua lại GitHub?", "vi"),
    ("Microsoft cân nhắc liệu có mua lại GitHub.", "vi"),
    ("Bill Gates acquired Microsoft.", "en"),
    ("Disney buys Pixar", "en"),
])
def test_abstains(nlp, text, lang):
    assert extract_relations(text, nlp.mentions(text, lang), lang) == []


def test_alias_and_span_boundaries(nlp):
    assert nlp.resolve("Disney", "ORG")["entity_id"] == nlp.resolve("The Walt Disney Company", "ORG")["entity_id"]
    assert not nlp.mentions("Microsoftish", "en")
    text = "The Walt Disney Company acquired Pixar."
    mentions = nlp.mentions(text, "en")
    assert mentions[0]["surface"] == "The Walt Disney Company"
    assert len(mentions) == 2
    assert nlp.resolve("Microsof", "ORG")["entity_id"] != nlp.resolve("Microsoft", "ORG")["entity_id"]
    assert nlp.suggestions("Microsof")


def test_document_person_aliases_use_unique_full_name_anchor():
    entities = {
        "elon": {"name": "Elon Musk", "entity_type": "PERSON"},
        "musk-person": {"name": "Musk", "entity_type": "PERSON"},
        "musk-org": {"name": "Musk", "entity_type": "ORG"},
    }
    mentions = [
        {"entity_id": "elon", "surface": "Elon Musk"},
        {"entity_id": "musk-person", "surface": "Ông Musk"},
        {"entity_id": "musk-org", "surface": "Musk"},
    ]
    assert document_person_aliases(entities, mentions) == {
        "musk-person": "elon",
    }


def test_document_person_aliases_abstain_when_surname_is_ambiguous():
    entities = {
        "elon": {"name": "Elon Musk", "entity_type": "PERSON"},
        "kimbal": {"name": "Kimbal Musk", "entity_type": "PERSON"},
        "musk": {"name": "Musk", "entity_type": "PERSON"},
    }
    mentions = [{"entity_id": key, "surface": entity["name"]}
                for key, entity in entities.items()]
    assert document_person_aliases(entities, mentions) == {}


def test_offsets_unicode_and_language(nlp):
    text = normalize("  Microsoft\u00a0đã mua lại GitHub.\nBill Gates thành lập Microsoft!")
    for sentence in sentences(text):
        assert text[sentence["start"]:sentence["end"]] == sentence["text"]
        for mention in nlp.mentions(sentence["text"], "vi"):
            assert sentence["text"][mention["start"]:mention["end"]] == mention["surface"]
    assert route(text, "vi")[0] == "vi"
    assert route("")[0] == "unknown"
    assert nlp.mentions("Microsoft", "unknown") == []
    assert stable_id("a|b", "c") != stable_id("a", "b|c")


def test_sentence_decimal_and_last_fragment():
    text = "The deal is worth $7.4 billion. Last fragment\nNew line."
    assert [s["text"] for s in sentences(text)] == [
        "The deal is worth $7.4 billion.", "Last fragment", "New line."]


class FakeRelex:
    def __init__(self, entities, relations):
        self.entities, self.relations = entities, relations
        self.calls = 0

    def inference(self, **kwargs):
        self.calls += 1
        return [self.entities], [self.relations]


@pytest.mark.parametrize("text,language,entities,relations,predicate,subject,object_", [
    ("Microsoft invested in GitHub.", "en", [
        {"start": 0, "end": 9, "text": "Microsoft", "label": "organization", "score": 0.9},
        {"start": 22, "end": 28, "text": "GitHub", "label": "organization", "score": 0.9},
    ], [{"head": {"start": 0, "end": 9}, "tail": {"start": 22, "end": 28},
         "relation": "invested in", "score": 0.9}], "INVESTED_IN", "Microsoft", "GitHub"),
    ("Vingroup đầu tư vào Microsoft.", "vi", [
        {"start": 0, "end": 8, "text": "Vingroup", "label": "tổ chức", "score": 0.9},
        {"start": 20, "end": 29, "text": "Microsoft", "label": "tổ chức", "score": 0.9},
    ], [{"head": {"start": 0, "end": 8}, "tail": {"start": 20, "end": 29},
         "relation": "đầu tư vào", "score": 0.9}], "INVESTED_IN", "Vingroup", "Microsoft"),
])
def test_gliner_joint_extraction_maps_both_languages_once(
        nlp, text, language, entities, relations, predicate, subject, object_):
    from unittest.mock import patch
    nlp.backend = "models"
    model = FakeRelex(entities, relations)
    nlp.models[language] = model
    mentions = nlp.mentions(text, language)
    with patch("weconomy.nlp.extract_relations", return_value=[]):
        claims = nlp.relations(text, mentions, language)
    assert len(claims) == 1
    assert claims[0]["predicate"] == predicate
    assert claims[0]["subject_id"] == nlp.resolve(subject, "ORG")["entity_id"]
    assert claims[0]["object_id"] == nlp.resolve(object_, "ORG")["entity_id"]
    assert model.calls == 1


def test_gliner_aliases_keep_curated_entity_types(nlp):
    nlp.backend = "models"
    nlp.models["vi"] = FakeRelex(
        [{"start": 0, "end": 20, "text": "Pháp Emmanuel Macron", "label": "địa điểm", "score": 0.9}], [])
    found = nlp.mentions("Pháp Emmanuel Macron", "vi")
    assert [(m["surface"], m["entity"]["entity_type"]) for m in found] == [
        ("Pháp", "GOV"), ("Emmanuel Macron", "PERSON")]


def test_acquisition_agreement_is_not_a_completed_acquisition(nlp):
    text = "Microsoft has agreed to acquire GitHub."
    claims = extract_relations(text, nlp.mentions(text, "en"), "en")
    assert len(claims) == 1
    assert claims[0]["predicate"] == "AGREED_TO_ACQUIRE"
    assert claims[0]["assertion_status"] == "agreement_reported"
    assert not any(r["predicate"] == "ACQUIRED" for r in claims)
    vi = "Microsoft đã đạt thỏa thuận mua lại GitHub."
    assert extract_relations(vi, nlp.mentions(vi, "vi"), "vi")[0]["predicate"] == "AGREED_TO_ACQUIRE"
    negated = "Microsoft has not agreed to acquire GitHub."
    assert not extract_relations(negated, nlp.mentions(negated, "en"), "en")


def test_abbreviation_does_not_cut_evidence_mid_sentence():
    text = "A company serves the U.S. military. It has an office."
    assert [s["text"] for s in sentences(text)] == [
        "A company serves the U.S. military.", "It has an office."]


@pytest.mark.parametrize("text,lang,predicate,subject,object_", [
    ("GitHub was acquired by Microsoft.", "en", "ACQUIRED", "Microsoft", "GitHub"),
    ("Microsoft was founded by Bill Gates.", "en", "FOUNDED", "Bill Gates", "Microsoft"),
    ("Microsoft CEO Bill Gates spoke today.", "en", "CEO_OF", "Bill Gates", "Microsoft"),
    ("Microsoft’s CEO Bill Gates spoke today.", "en", "CEO_OF", "Bill Gates", "Microsoft"),
    ("GitHub was sued by Microsoft.", "en", "SUED", "Microsoft", "GitHub"),
    ("GitHub đã được mua lại bởi Microsoft.", "vi", "ACQUIRED", "Microsoft", "GitHub"),
    ("Microsoft được thành lập bởi Bill Gates.", "vi", "FOUNDED", "Bill Gates", "Microsoft"),
])
def test_reverse_relations_keep_semantic_direction(nlp, text, lang, predicate, subject, object_):
    claims = extract_relations(text, nlp.mentions(text, lang), lang)
    assert len(claims) == 1
    assert claims[0]["predicate"] == predicate
    assert claims[0]["subject_id"] == nlp.resolve(subject, "PERSON" if subject == "Bill Gates" else "ORG")["entity_id"]
    assert claims[0]["object_id"] == nlp.resolve(object_, "ORG")["entity_id"]


@pytest.mark.parametrize("text", [
    "GitHub will be acquired by Microsoft.", "GitHub was not acquired by Microsoft.",
    "GitHub may have been acquired by Microsoft.", "Microsoft former CEO Bill Gates spoke today.",
    "GitHub was founded by Microsoftish.",
])
def test_reverse_rules_abstain_on_plans_negation_and_wrong_endpoints(nlp, text):
    assert not extract_relations(text, nlp.mentions(text, "en"), "en")


@pytest.mark.parametrize("text", [
    "Bill Gates, co-founder and CEO of Microsoft, spoke today.",
    "Microsoft co-founder and CEO Bill Gates spoke today.",
    "“A product,” said Microsoft founder and CEO Bill Gates.",
    "The product is available,” Microsoft founder and CEO Bill Gates said.",
])
def test_explicit_combined_roles_keep_two_distinct_relations(nlp, text):
    claims = extract_relations(text, nlp.mentions(text, "en"), "en")
    assert {c["predicate"] for c in claims} == {"CEO_OF", "FOUNDED"}
    assert len(claims) == 2
    assert all(c["subject_id"] == nlp.resolve("Bill Gates", "PERSON")["entity_id"] for c in claims)
    assert all(c["object_id"] == nlp.resolve("Microsoft", "ORG")["entity_id"] for c in claims)


@pytest.mark.parametrize("text", [
    "“Microsoft founder and CEO Bill Gates spoke today.”",
    '"Microsoft founder and CEO Bill Gates spoke today."',
    'The phrase “Microsoft founder and CEO Bill Gates” is an example.',
    "Microsoft former founder and CEO Bill Gates spoke today.",
    "Bill Gates, Principal at Microsoft, spoke today.",
    "Bill Gates, Managing Partner at Microsoft, spoke today.",
])
def test_roles_do_not_invent_ceo_from_other_jobs_or_quoted_claims(nlp, text):
    assert not extract_relations(text, nlp.mentions(text, "en"), "en")
