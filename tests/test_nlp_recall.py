"""Recall regressions from saved corpus review and explicit relation patterns."""
from pathlib import Path

import pytest

from weconomy.nlp import NLP, extract_relations
from weconomy.pipeline import load_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def nlp():
    return NLP(load_config(ROOT / "config/pipeline.yaml"))


def claims(nlp, text, language):
    return extract_relations(text, nlp.mentions(text, language), language)


@pytest.mark.parametrize("text,predicate,person,org", [
    ("Satya Nadella là CEO của Microsoft.", "CEO_OF", "Satya Nadella", "Microsoft"),
    ("Satya Nadella, tổng giám đốc của Microsoft.", "CEO_OF", "Satya Nadella", "Microsoft"),
    ("Satya Nadella, giám đốc điều hành của Microsoft.", "CEO_OF", "Satya Nadella", "Microsoft"),
    ("Satya Nadella, nhà sáng lập Microsoft.", "FOUNDED", "Satya Nadella", "Microsoft"),
    ("Microsoft, công ty con của Apple.", "SUBSIDIARY_OF", "Microsoft", "Apple"),
    ("Microsoft là công ty con của Apple.", "SUBSIDIARY_OF", "Microsoft", "Apple"),
])
def test_vietnamese_named_roles_and_subsidiary_direction(nlp, text, predicate, person, org):
    found = claims(nlp, text, "vi")
    wanted_subject = person if predicate == "FOUNDED" else person
    wanted_object = org
    assert len(found) == 1
    assert found[0]["predicate"] == predicate
    assert found[0]["subject_id"] == nlp.resolve(wanted_subject, "ORG" if predicate == "SUBSIDIARY_OF" else "PERSON")["entity_id"]
    assert found[0]["object_id"] == nlp.resolve(wanted_object, "ORG")["entity_id"]


@pytest.mark.parametrize("text", [
    "Microsoft CEO Satya Nadella.",
    "Satya Nadella - CEO của Microsoft.",
])
def test_vietnamese_ceo_role_accepts_unpunctuated_reverse_and_ascii_hyphen(nlp, text):
    found = claims(nlp, text, "vi")
    assert len(found) == 1
    assert found[0]["predicate"] == "CEO_OF"
    assert found[0]["subject_id"] == nlp.resolve("Satya Nadella", "PERSON")["entity_id"]
    assert found[0]["object_id"] == nlp.resolve("Microsoft", "ORG")["entity_id"]


@pytest.mark.parametrize("text", [
    "Satya Nadella, giám đốc của Microsoft.",
    "Satya Nadella, chủ tịch của Microsoft.",
    "Satya Nadella và Microsoft công bố kế hoạch.",
])
def test_vietnamese_roles_do_not_conflate_director_chairman_or_conjunction(nlp, text):
    assert not claims(nlp, text, "vi")


def test_vietnamese_combined_role_produces_separate_typed_claims(nlp):
    text = "Satya Nadella, nhà sáng lập và CEO của Microsoft."
    found = claims(nlp, text, "vi")
    assert {claim["predicate"] for claim in found} == {"FOUNDED", "CEO_OF"}
    assert all(claim["subject_id"] == nlp.resolve("Satya Nadella", "PERSON")["entity_id"] for claim in found)
    assert all(claim["object_id"] == nlp.resolve("Microsoft", "ORG")["entity_id"] for claim in found)


def test_funding_round_named_leads_and_participants_point_to_receiver(nlp):
    text = ("Microsoft raised $20 million in a Series A round led by Apple and co-led by Salesforce, "
            "with participation from LinkedIn.")
    found = claims(nlp, text, "en")
    assert {(c["subject_id"], c["object_id"]) for c in found} == {
        (nlp.resolve(name, "ORG")["entity_id"], nlp.resolve("Microsoft", "ORG")["entity_id"])
        for name in ("Apple", "Salesforce", "LinkedIn")
    }
    assert all(c["predicate"] == "INVESTED_IN" for c in found)
    assert all(c["rule_id"] == "en-INVESTED_IN-funding-round-v1" for c in found)
    assert {c["trigger"] for c in found} == {"led by", "with participation from"}


@pytest.mark.parametrize("text", [
    "Microsoft raised debt in a Series A round led by Apple.",
    "Microsoft secured a loan through a Series A round led by Apple.",
    "Microsoft raised its target for a Series A round led by Apple.",
    "Microsoft raised a proposed Series A round led by Apple.",
    "Microsoft raised a failed Series A round led by Apple.",
    "Microsoft plans to raise a Series A round led by Apple.",
    "Microsoft may have raised a Series A round led by Apple.",
    "Microsoft did not raise a Series A round led by Apple.",
    '"Microsoft raised a Series A round led by Apple."',
    "Microsoft raised a Series A round led by it.",
    "Microsoft raised a Series A round. It was led by Apple.",
    "Apple announced that Microsoft raised a Series A round led by Apple.",
])
def test_funding_round_abstains_on_nonasserted_unresolved_or_wrong_scope(nlp, text):
    assert not claims(nlp, text, "en")


def test_funding_round_deduplicates_same_named_investor(nlp):
    text = "Microsoft raised a seed round led by Apple, with participation from Apple."
    found = claims(nlp, text, "en")
    assert len(found) == 1
    assert found[0]["subject_id"] == nlp.resolve("Apple", "ORG")["entity_id"]
    assert found[0]["object_id"] == nlp.resolve("Microsoft", "ORG")["entity_id"]


def test_english_role_claims_survive_coordination_after_the_object(nlp):
    text = "Apple CEO Satya Nadella and Microsoft founder Bill Gates."
    found = claims(nlp, text, "en")
    assert {(c["predicate"], c["subject_id"], c["object_id"]) for c in found} == {
        ("CEO_OF", nlp.resolve("Satya Nadella", "PERSON")["entity_id"], nlp.resolve("Apple", "ORG")["entity_id"]),
        ("FOUNDED", nlp.resolve("Bill Gates", "PERSON")["entity_id"], nlp.resolve("Microsoft", "ORG")["entity_id"]),
    }


def test_role_founder_requires_person_but_explicit_founded_verb_keeps_org_subject(nlp):
    assert not claims(nlp, "Apple founder Microsoft.", "en")
    true_role = claims(nlp, "Apple founder Bill Gates.", "en")
    assert [claim["predicate"] for claim in true_role] == ["FOUNDED"]
    explicit = claims(nlp, "Microsoft founded Apple.", "en")
    assert len(explicit) == 1 and explicit[0]["predicate"] == "FOUNDED"


@pytest.mark.parametrize("text", [
    "“Apple CEO Satya Nadella and Microsoft founder Bill Gates.”",
    "Apple did not name Satya Nadella CEO of Microsoft.",
    "Microsoft acquired Apple and GitHub.",
])
def test_role_coordination_does_not_override_quotes_negation_or_verb_coordination(nlp, text):
    assert not claims(nlp, text, "en")
