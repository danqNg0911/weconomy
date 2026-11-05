"""Artificial sentences here are software fixtures, never corpus news."""
from pathlib import Path

import pytest

from weconomy.nlp import (
    NLP,
    align_token,
    dependency_relations_vi,
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
    ("Microsoft đã mua lại GitHub.", "vi", "ACQUIRED"),
    ("Microsoft đã đầu tư vào GitHub.", "vi", "INVESTED_IN"),
    ("Bill Gates thành lập Microsoft.", "vi", "FOUNDED"),
])
def test_direct_rules(nlp, text, lang, predicate):
    found = extract_relations(text, nlp.mentions(text, lang), lang)
    assert len(found) == 1
    assert found[0]["predicate"] == predicate
    assert found[0]["subject_id"] != found[0]["object_id"]


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


def test_vietnamese_tokenizer_inserted_quote_spaces_keep_original_offsets(nlp):
    # Underthesea can return a token '‘ quân' for source '‘quân'. Token spacing is not source spacing.
    nlp.backend = "models"
    nlp.vi_ner = lambda _: [
        ("Vingroup", "N", "B-NP", "B-ORG"), ("có", "V", "B-VP", "O"),
        ("‘ quân", "N", "B-NP", "O"), ("bài ’", "N", "I-NP", "O"),
        ("mới", "A", "B-AP", "O"), (".", "CH", "O", "O"),
    ]
    text = "Vingroup có ‘quân bài’ mới."
    found = nlp.mentions(text, "vi")
    assert [(m["surface"], m["start"], m["end"]) for m in found] == [("Vingroup", 0, 8)]


def test_alignment_does_not_jump_over_source_words_or_change_letters():
    with pytest.raises(ValueError, match="offsets"):
        align_token("Other Microsoft", "Microsoft", 0)
    with pytest.raises(ValueError, match="offsets"):
        align_token("Vingroup", "Vingroub", 0)
    assert align_token("Hồ Chí Minh", "Hồ_Chí_Minh", 0) == (0, 11)
    assert align_token("name_with_underscore", "name_with_underscore", 0) == (0, 20)
    assert align_token("Tuỳ vào", "Tùy", 0) == (0, 3)
    assert align_token("Hoà Bình", "Hòa Bình", 0) == (0, 8)
    with pytest.raises(ValueError):
        align_token("Túy", "Tùy", 0)  # A different tone is not spelling normalization.


@pytest.fixture(scope="module")
def model_nlp():
    pytest.importorskip("en_core_web_sm")
    result = NLP(load_config(ROOT / "config/pipeline.yaml"))
    import spacy
    result.backend = "models"
    result.en = spacy.load("en_core_web_sm")
    return result


@pytest.mark.parametrize("text,predicate,subject,object_", [
    ("Microsoft recently acquired GitHub.", "ACQUIRED", "Microsoft", "GitHub"),
    ("GitHub was recently acquired by Microsoft.", "ACQUIRED", "Microsoft", "GitHub"),
    ("Bill Gates founded Microsoft in 1975.", "FOUNDED", "Bill Gates", "Microsoft"),
    ("Microsoft invested heavily in GitHub.", "INVESTED_IN", "Microsoft", "GitHub"),
    ("Microsoft acquired GitHub.", "ACQUIRED", "Microsoft", "GitHub"),
    ("Microsoft has acquired software company GitHub, the companies announced on Tuesday.",
     "ACQUIRED", "Microsoft", "GitHub"),
    ("Microsoft announced that Apple recently acquired GitHub.", "ACQUIRED", "Apple", "GitHub"),
])
def test_model_dependency_arguments_and_rule_dedup(model_nlp, text, predicate, subject, object_):
    found = model_nlp.relations(text, model_nlp.mentions(text, "en"), "en")
    assert len(found) == 1
    assert found[0]["predicate"] == predicate
    assert found[0]["subject_id"] == model_nlp.resolve(subject, "ORG")["entity_id"]
    assert found[0]["object_id"] == model_nlp.resolve(object_, "ORG")["entity_id"]


@pytest.mark.parametrize("text", [
    "Microsoft may acquire GitHub.", "Microsoft plans to acquire GitHub.",
    "Microsoft acquired a stake in GitHub.", "Microsoft acquired GitHub’s assets.",
    "Microsoft did not acquire GitHub.", "It acquired GitHub.",
    "Microsoft recently acquired GitHub and Apple.",
    "Microsoft denied that Apple acquired GitHub.",
    "Microsoft said Apple may acquire GitHub.",
    "Microsoft might announce that Apple recently acquired GitHub.",
    "Microsoft imagined Apple recently acquired GitHub.",
    "Microsoft announced that it recently acquired GitHub.",
])
def test_dependency_abstains_on_modal_partial_ownership_and_unresolved_subjects(model_nlp, text):
    from weconomy.nlp import dependency_relations
    mentions = model_nlp.mentions(text, "en")
    assert not dependency_relations(model_nlp.en(text), mentions)


def test_model_extracts_open_predicate_for_unlisted_explicit_relation(model_nlp):
    text = "Microsoft licenses technology to GitHub."
    mentions = model_nlp.mentions(text, "en")
    found = model_nlp.relations(text, mentions, "en")
    assert len(found) == 1
    assert found[0]["predicate"] == "LICENSE_TO"
    assert found[0]["trigger"] == "licenses"


def fake_vi_doc(text, rows):
    from types import SimpleNamespace
    words = [SimpleNamespace(id=i, text=token, lemma=lemma, head=head, deprel=dep,
                             start_char=start, end_char=end)
             for i, (token, lemma, head, dep, start, end) in enumerate(rows, 1)]
    return SimpleNamespace(text=text, sentences=[SimpleNamespace(words=words)])


@pytest.mark.parametrize("text,rows,predicate,subject,object_", [
    ("Microsoft gần đây đã mua lại GitHub.", [
        ("Microsoft", "Microsoft", 4, "nsubj", 0, 9), ("gần", "gần", 4, "advcl", 10, 13),
        ("đã", "đã", 4, "advmod", 18, 20), ("mua", "mua", 0, "root", 21, 24),
        ("lại", "lại", 4, "advmod", 25, 28), ("GitHub", "GitHub", 4, "obj", 29, 35),
    ], "ACQUIRED", "Microsoft", "GitHub"),
    ("GitHub đã được Microsoft mua lại.", [
        ("GitHub", "GitHub", 5, "nsubj:pass", 0, 6), ("đã", "đã", 5, "advmod", 7, 9),
        ("được", "được", 5, "aux:pass", 10, 14), ("Microsoft", "Microsoft", 5, "obl:agent", 15, 24),
        ("mua", "mua", 0, "root", 25, 28), ("lại", "lại", 5, "advmod", 29, 32),
    ], "ACQUIRED", "Microsoft", "GitHub"),
    ("Vingroup đầu tư vào Microsoft.", [
        ("Vingroup", "Vingroup", 2, "nsubj", 0, 8), ("đầu tư", "đầu tư", 0, "root", 9, 15),
        ("vào", "vào", 2, "compound:dir", 16, 19), ("Microsoft", "Microsoft", 3, "obj", 20, 29),
    ], "INVESTED_IN", "Vingroup", "Microsoft"),
])
def test_vietnamese_dependency_arguments(nlp, text, rows, predicate, subject, object_):
    found = dependency_relations_vi(fake_vi_doc(text, rows), nlp.mentions(text, "vi"))
    assert len(found) == 1
    assert found[0]["predicate"] == predicate
    assert found[0]["subject_id"] == nlp.resolve(subject, "ORG")["entity_id"]
    assert found[0]["object_id"] == nlp.resolve(object_, "ORG")["entity_id"]


def test_vietnamese_dependency_maps_explicit_request(nlp):
    text = "Microsoft đề nghị GitHub hợp tác."
    rows = [
        ("Microsoft", "Microsoft", 2, "nsubj", 0, 9), ("đề nghị", "đề nghị", 0, "root", 10, 17),
        ("GitHub", "GitHub", 2, "obj", 18, 24),
    ]
    found = dependency_relations_vi(fake_vi_doc(text, rows), nlp.mentions(text, "vi"))
    assert len(found) == 1 and found[0]["predicate"] == "REQUESTS"


def test_vietnamese_request_finds_country_inside_government_subject_and_coordination(nlp):
    text = "Chính quyền Mỹ đề nghị Pháp và Đức dùng kho dự trữ."
    rows = [
        ("Chính quyền", "chính quyền", 3, "nsubj", 0, 11), ("Mỹ", "Mỹ", 1, "nmod", 12, 14),
        ("đề nghị", "đề nghị", 0, "root", 15, 22), ("Pháp", "Pháp", 3, "obj", 23, 27),
        ("và", "và", 6, "cc", 28, 30), ("Đức", "Đức", 4, "conj", 31, 34),
    ]
    found = dependency_relations_vi(fake_vi_doc(text, rows), nlp.mentions(text, "vi"))
    expected_subject = nlp.resolve("United States", "GOV")["entity_id"]
    expected_objects = {nlp.resolve(name, "GOV")["entity_id"] for name in ("France", "Germany")}
    assert {(claim["subject_id"], claim["object_id"]) for claim in found} == {
        (expected_subject, object_id) for object_id in expected_objects}


def test_vietnamese_dependency_abstains_on_future_claim(nlp):
    text = "Microsoft sẽ mua lại GitHub."
    rows = [
        ("Microsoft", "Microsoft", 3, "nsubj", 0, 9), ("sẽ", "sẽ", 3, "advmod", 10, 13),
        ("mua", "mua", 0, "root", 14, 17), ("lại", "lại", 3, "advmod", 18, 21),
        ("GitHub", "GitHub", 3, "obj", 22, 28),
    ]
    assert not dependency_relations_vi(fake_vi_doc(text, rows), nlp.mentions(text, "vi"))


def test_curated_vietnamese_country_aliases_override_overlapping_ner(nlp):
    nlp.backend = "models"
    nlp.vi_ner = lambda _: [("Pháp Emmanuel Macron", "Np", "B-NP", "B-LOC")]
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
