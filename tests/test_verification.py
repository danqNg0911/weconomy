import pytest

from weconomy.entity_quality import entity_name_issue, named_head
from weconomy.nlp import relation_label_candidates, supported_relation


@pytest.mark.parametrize("name,issue", [
    ("Series H", "financing_round_not_organization"),
    ("$1 billion Series H", "financing_round_not_organization"),
    ("Model 3", "product_not_organization"),
    ("TechCrunch Disrupt 2026", "event_not_organization"),
    ("Kế hoạch", "generic_or_pronominal"),
    ("AI labs", "generic_or_pronominal"),
    ("165 AI-native companies", "generic_or_pronominal"),
    ("AI coding startup", "generic_or_pronominal"),
    ("FDA-approved human stem cell therapy", "generic_or_pronominal"),
    ("Multiple families", "generic_or_pronominal"),
    ("VCs", "generic_or_pronominal"),
    ("The VCs", "generic_or_pronominal"),
    ("European entrepreneurs", "generic_or_pronominal"),
    ("Asian investors", "generic_or_pronominal"),
    ("LPs", "generic_or_pronominal"),
    ("the GPs", "generic_or_pronominal"),
    ("SaaS firms", "generic_or_pronominal"),
    ("Fund I", "unnamed_fund_vehicle"),
    ("new fundraising", "lowercase_unverified_name"),
    ("xAI", None), ("eBay", None), ("Series X Capital", None),
])
def test_names_are_checked_by_meaning_and_case(name, issue):
    assert entity_name_issue(name, "ORG") == issue


def test_curated_lowercase_brand_and_explicit_named_head():
    assert entity_name_issue("n8n", "ORG", curated=True) is None
    assert named_head("financial services startup Coterie") == "Coterie"
    assert named_head("AI agent startup Manus") == "Manus"
    assert named_head("window-cleaning robot startup Lucid Bots") == "Lucid Bots"
    assert named_head("Series X Capital") == "Series X Capital"
    assert named_head("Founders Fund") == "Founders Fund"
    assert named_head("Indian conglomerate HCL Group") == "HCL Group"
    assert named_head("Fusion startup Inertia Enterprises") == "Inertia Enterprises"
    assert named_head("Defense startup Firestorm Labs") == "Firestorm Labs"
    assert named_head("Window-cleaning robot startup Lucid Bots") == "Lucid Bots"
    assert named_head("David Sacks’ firm Craft Ventures") == "Craft Ventures"
    assert named_head("xã hội X") == "X"


def test_founders_employer_is_not_the_founder_of_another_company():
    from weconomy.nlp import extract_relations

    text = "Neko was founded by Spotify co-founder and CEO Daniel Ek."
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name), "surface": name,
                 "entity": {"entity_id": name, "entity_type": kind}}
                for name, kind in [("Neko", "ORG"), ("Spotify", "ORG"), ("Daniel Ek", "PERSON")]]
    assert not supported_relation(text, mentions, "en", "FOUNDED", "Spotify", "Neko")
    assert not any(row["predicate"] == "FOUNDED" and row["subject_id"] == "Spotify"
                   for row in extract_relations(text, mentions, "en"))
    text = "Neko was founded by Spotify."
    assert supported_relation(text, mentions[:2], "en", "FOUNDED", "Spotify", "Neko")


@pytest.mark.parametrize("organization", ["Northstar", "Helix", "Tide"])
@pytest.mark.parametrize("role", ["co-founder", "founder", "CEO", "chief executive officer"])
def test_person_role_guard_is_independent_of_company_names(organization, role):
    text = f"Juniper was founded by {organization} {role} Jane Doe."
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name), "surface": name,
                 "entity": {"entity_id": name, "entity_type": kind}}
                for name, kind in [("Juniper", "ORG"), (organization, "ORG"), ("Jane Doe", "PERSON")]]
    assert not supported_relation(text, mentions, "en", "FOUNDED", organization, "Juniper")


@pytest.mark.parametrize("text,expected", [
    ("Northstar CEO Jane Doe spoke.", False),
    ("Former Northstar CEO Jane Doe spoke.", True),
    ("Northstar ex-CEO Jane Doe spoke.", True),
    ("Jane Doe, former CEO of Northstar, spoke.", True),
    ("Cựu CEO Northstar Jane Doe phát biểu.", True),
    ("Jane Doe, cựu tổng giám đốc của Northstar, phát biểu.", True),
    ("A former Helix CEO met Northstar CEO Jane Doe.", False),
])
def test_historical_role_is_attached_to_the_named_pair(text, expected):
    from weconomy.entity_quality import historical_role

    rows = [{"start": text.index(name), "end": text.index(name) + len(name)} for name in ("Jane Doe", "Northstar")]
    assert historical_role(text, *rows) is expected


@pytest.mark.parametrize("text,predicate,expected", [
    ('“We had no competition,” Acme CEO Jane Doe said.', "CEO_OF", True),
    ('“Terminals are not thinking tools,” Jane Doe, co-founder of Acme, said.', "FOUNDED", True),
    ('Acme CEO Jane Doe was not at the event.', "CEO_OF", True),
    ('In May, Acme CEO Jane Doe spoke.', "CEO_OF", True),
    ('While there, she met future industry leaders like Acme founder Jane Doe.', "FOUNDED", True),
    ('The future Acme CEO Jane Doe spoke.', "CEO_OF", False),
    ('Jane Doe is not the CEO of Acme.', "CEO_OF", False),
    ('It is not true that Acme CEO Jane Doe spoke.', "CEO_OF", False),
    ('If Acme CEO Jane Doe spoke, it would matter.', "CEO_OF", False),
    ('“Acme CEO Jane Doe is an example,” the author said.', "CEO_OF", False),
])
def test_unrelated_quoted_negation_does_not_suppress_asserted_roles(text, predicate, expected):
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name), "surface": name,
                 "entity": {"entity_id": name, "entity_type": kind}}
                for name, kind in [("Acme", "ORG"), ("Jane Doe", "PERSON")]]
    mentions.sort(key=lambda row: row["start"])
    assert supported_relation(text, mentions, "en", predicate, "Jane Doe", "Acme") is expected


@pytest.mark.parametrize("text,expected", [
    ("(Acme was acquired in 2023 by another eVTOL company, Globex.)", True),
    ("Acme was not acquired by Globex.", False),
    ("Acme was reportedly acquired by Globex.", False),
    ("Acme, a startup founded by Jane Doe, announced on Thursday that it has acquired the French startup Globex.", True),
    ("Acme, a startup founded by Jane Doe, announced on Thursday that it might acquire the French startup Globex.", False),
    ("Acme, a startup founded by Jane Doe, announced on Thursday that it has acquired the assets of startup Globex.", False),
])
def test_bounded_descriptions_do_not_change_acquisition_direction_or_certainty(text, expected):
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name), "surface": name,
                 "entity": {"entity_id": name, "entity_type": kind}}
                for name, kind in [("Acme", "ORG"), ("Globex", "ORG")]]
    mentions.sort(key=lambda row: row["start"])
    subject, object_ = ("Globex", "Acme") if "was " in text else ("Acme", "Globex")
    assert supported_relation(text, mentions, "en", "ACQUIRED", subject, object_) is expected


@pytest.mark.parametrize("possessive", ["’", "'", "’s", "'s"])
def test_named_parent_is_not_the_child_or_other_possessive_person_reference(possessive):
    text = f"Acme, the startup co-founded by John Jones{possessive} daughter, Jane Doe, launched today."
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name), "surface": name,
                 "entity": {"entity_id": name, "entity_type": kind}}
                for name, kind in [("Acme", "ORG"), ("John Jones", "PERSON"), ("Jane Doe", "PERSON")]]
    assert not supported_relation(text, mentions, "en", "FOUNDED", "John Jones", "Acme")


@pytest.mark.parametrize("text,predicate,reverse,expected", [
    ("Acme announced a partnership with Globex.", "PARTNERED_WITH", False, True),
    ("Acme attended a program at Globex.", "SUBSIDIARY_OF", False, False),
    ("Acme brings its chips to Globex.", "MERGED_WITH", False, False),
    ("Acme was acquired by Globex.", "ACQUIRED", False, False),
    ("Acme was acquired by Globex.", "ACQUIRED", True, True),
    ("Acme agreed to acquire Globex.", "ACQUIRED", False, False),
    ("Acme agreed to acquire Globex.", "AGREED_TO_ACQUIRE", False, True),
    ("Acme acquired a 10% stake in Globex.", "ACQUIRED", False, False),
    ("Acme acquired a 10% stake in Globex.", "OWNS_STAKE_IN", False, True),
    ("Acme is not a subsidiary of Globex.", "SUBSIDIARY_OF", False, False),
    ("Acme may have acquired Globex.", "ACQUIRED", False, False),
    ("Acme was led by Globex.", "INVESTED_IN", True, False),
])
def test_model_predicates_need_correct_semantic_direction(text, predicate, reverse, expected):
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name),
                 "entity": {"entity_id": name, "entity_type": "ORG"}} for name in ("Acme", "Globex")]
    subject, object_ = ("Globex", "Acme") if reverse else ("Acme", "Globex")
    assert supported_relation(text, mentions, "en", predicate, subject, object_) is expected


def test_model_is_not_asked_to_hallucinate_predicates_without_cues():
    assert relation_label_candidates("Acme brings its chips to Globex.", "en") == []
    assert relation_label_candidates("Acme invested in Globex.", "en") == ["invested in"]


def test_considering_a_merger_is_not_a_completed_merger():
    text = "Hồi tháng 1, Bloomberg từng đưa tin SpaceX đã cân nhắc sáp nhập với Tesla trước khi quyết định mua lại xAI."
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name),
                 "entity": {"entity_id": name, "entity_type": "ORG"}} for name in ("SpaceX", "Tesla", "xAI")]
    assert not supported_relation(text, mentions, "vi", "MERGED_WITH", "SpaceX", "Tesla")


def test_a_foundation_is_not_its_parent_company_and_a_company_owner_is_not_the_company():
    text = "Ron Conway has been on the board of the Salesforce Foundation."
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name),
                 "entity": {"entity_id": name, "entity_type": kind}}
                for name, kind in [("Ron Conway", "PERSON"), ("Salesforce", "ORG")]]
    assert not supported_relation(text, mentions, "en", "BOARD_MEMBER_OF", "Ron Conway", "Salesforce")
    text = "Nvidia đều sở hữu cổ phần tại công ty tên lửa của tỷ phú Elon Musk."
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name),
                 "entity": {"entity_id": name, "entity_type": "ORG"}} for name in ("Nvidia", "Elon Musk")]
    assert not supported_relation(text, mentions, "vi", "OWNS_STAKE_IN", "Nvidia", "Elon Musk")


@pytest.mark.parametrize("text,predicate,language,subject,object_", [
    ("Công ty đứng sau Acme đầu tư vào Globex.", "INVESTED_IN", "vi", "Acme", "Globex"),
    ("Một công ty con của MSC đã đồng ý mua cổ phần tại Sinokor.", "OWNS_STAKE_IN", "vi", "MSC", "Sinokor"),
    ("A subsidiary of MSC acquired Sinokor.", "ACQUIRED", "en", "MSC", "Sinokor"),
    ("Naive supplies a prompt that developers can provide to tools like Cursor.", "SUPPLIES_TO", "en", "Naive", "Cursor"),
])
def test_owners_planned_stakes_and_tool_compatibility_do_not_create_business_edges(
        text, predicate, language, subject, object_):
    mentions = [{"start": text.index(name), "end": text.index(name) + len(name),
                 "entity": {"entity_id": name, "entity_type": "ORG"}} for name in (subject, object_)]
    assert not supported_relation(text, mentions, language, predicate, subject, object_)
