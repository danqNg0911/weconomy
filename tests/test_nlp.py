"""Artificial sentences here are software fixtures, never corpus news."""
from pathlib import Path

import pytest

from weconomy.nlp import NLP, extract_relations, normalize, route, sentences
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
    ("Microsoft đã mua lại GitHub.", "vi", "ACQUIRED"),
    ("Microsoft đã đầu tư vào GitHub.", "vi", "INVESTED_IN"),
    ("Bill Gates thành lập Microsoft.", "vi", "FOUNDED"),
])
def test_direct_rules(nlp, text, lang, predicate):
    found = extract_relations(text, nlp.mentions(text, lang), lang)
    assert len(found) == 1
    assert found[0]["predicate"] == predicate
    assert found[0]["subject_id"] != found[0]["object_id"]


@pytest.mark.parametrize("text,lang", [
    ("Microsoft did not acquire GitHub.", "en"),
    ("If Microsoft acquired GitHub, costs would rise.", "en"),
    ("Microsoft reportedly acquired GitHub.", "en"),
    ('"Microsoft acquired GitHub," the rumour said.', "en"),
    ("Microsoft and GitHub made announcements.", "en"),
    ("Microsoft plans to acquire GitHub.", "en"),
    ("Microsoft acquired shares in GitHub.", "en"),
    ("Microsoft chưa mua lại GitHub.", "vi"),
    ("Nếu Microsoft mua lại GitHub, họ sẽ thay đổi.", "vi"),
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
