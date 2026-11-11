from weconomy.funding import funding_references
from weconomy.nlp import sentences
from weconomy.schema import stable_id


def test_generic_funding_and_explicit_investor_list_do_not_require_a_series_label():
    text = ("Acme has raised over $30 million in funding at a $94 million valuation. "
            "Its investors include Atlas Ventures and Beacon Capital.")
    result = recover(text)
    assert len(result["claims"]) == 2
    assert {row["rule_id"] for row in result["claims"]} == {"en-explicit-investor-reference-v1"}
    assert all(text[row["evidence_start"]:row["evidence_end"]] == row["evidence"] for row in result["claims"])


def test_generic_funding_does_not_turn_debt_grants_or_distant_pronouns_into_equity_rounds():
    for kind in ("debt funding", "grant funding", "convertible funding"):
        text = f"Acme raised $30 million in {kind}. Its investors include Atlas Ventures."
        assert not recover(text)["claims"]
    text = "Acme raised $30 million in funding. The round was led by Atlas Ventures."
    assert not recover(text)["claims"]
    text = ("Acme raised $30 million in funding. Globex announced a product. "
            "Its investors include Atlas Ventures.")
    assert not recover(text, ("Acme", "Globex"))["claims"]


def test_inline_round_is_not_confused_with_a_pronominal_investor_list():
    text = "Its main competitor, Acme, raised a $19 million Series A co-led by Atlas Ventures."
    assert len(recover(text)["claims"]) == 1


def test_completed_round_announcements_and_named_investor_descriptions():
    for text in [
        "Acme announced on Friday a $13 million Series A round led by Atlas Ventures.",
        "Acme is backed by $9 million in seed funding led by Atlas Ventures.",
        "Acme raised $13 million in a Series A round. The funding round was led by private equity firm Atlas Ventures.",
    ]:
        result = recover(text, ("Acme", "Atlas Ventures"))
        assert len(result["claims"]) == 1
        assert result["claims"][0]["subject_id"] == stable_id("ORG", "atlas ventures")
        assert text[result["claims"][0]["evidence_start"]:result["claims"][0]["evidence_end"]] == result["claims"][0]["evidence"]
    assert not recover("Acme announced plans for a $13 million Series A round led by Atlas Ventures.")["claims"]


def test_company_funding_reference_is_bound_only_to_a_unique_adjacent_recipient():
    text = ("Acme is building a fire protection system. "
            "The company has raised $15 million in a Series A round led by Atlas Ventures.")
    result = recover(text)
    assert len(result["claims"]) == 1
    assert result["claims"][0]["object_id"] == stable_id("ORG", "acme")
    assert result["claims"][0]["evidence"] == text
    ambiguous = text.replace("Acme is building", "Acme and Globex are building")
    assert not recover(ambiguous, ("Acme", "Globex"))["claims"]
    separated = text.replace("system. ", "system.\n\n")
    assert not recover(separated)["claims"]
    unrelated = text.replace("The company", "Its competitor")
    assert not recover(unrelated)["claims"]


def test_company_behind_a_product_is_not_the_named_product_receiving_capital():
    text = ("ProductHub launched today. The company behind ProductHub announced a $9 million "
            "seed round led by Atlas Ventures.")
    assert not recover(text, ("ProductHub",))["claims"]


def test_referent_is_not_the_previous_rounds_investor_or_an_incidental_object():
    for preceding in ("The round was led by Atlas Ventures.", "Atlas Ventures led the round."):
        text = preceding + " The company raised $15 million in a Series A round led by Beacon Capital."
        assert not recover(text, ("Atlas Ventures",))["claims"]
    text = "A software tool integrates with Acme. The company raised $15 million in a Series A round led by Atlas Ventures."
    assert not recover(text)["claims"]
    text = "John and Jane launched Acme. The startup raised $15 million in a Series A round led by Atlas Ventures."
    assert len(recover(text)["claims"]) == 1


def test_employee_investors_do_not_turn_their_employers_into_investors():
    text = ("Acme raised $15 million in a Series A round. "
            "Other investors include Atlas Ventures and operators from companies like Globex, Initech, and Umbrella.")
    result = recover(text, ("Acme", "Atlas Ventures", "Globex", "Initech", "Umbrella"))
    assert len(result["claims"]) == 1
    assert result["claims"][0]["subject_id"] == stable_id("ORG", "atlas ventures")


def test_completed_unnumbered_round_has_explicit_lead_without_becoming_a_debt_round():
    text = ("Acme makes fire protection systems. The company has raised a $15 million round "
            "led by The O.H.I.O. Fund with participation from Khosla Ventures.")
    result = recover(text)
    assert len(result["claims"]) == 2
    assert {row["name"] for row in result["entities"]} == {"The O.H.I.O. Fund", "Khosla Ventures"}
    assert all(text[row["evidence_start"]:row["evidence_end"]] == row["evidence"] for row in result["claims"])
    assert not recover("Acme raised $15 million in a debt round led by Atlas Ventures.")["claims"]


def recover(text, company_names=("Acme",)):
    entities = {stable_id("ORG", name.casefold()): {"entity_id": stable_id("ORG", name.casefold()),
                "name": name, "entity_type": "ORG"} for name in company_names}
    mentions = [{"entity_id": entity_id, "entity_type": "ORG", "start": text.index(row["name"]),
                 "end": text.index(row["name"]) + len(row["name"]), "surface": row["name"]}
                for entity_id, row in entities.items()]
    return funding_references(text, "doc", list(sentences(text)), mentions, entities)


def test_round_reference_links_explicit_investors_without_inventing_manager_investments():
    text = ("Acme, a London-based robotics startup, has raised $30 million in a Series B round. "
            "The round was led by Atlas Ventures. "
            "Other investors in this round include Beacon Capital, Birch Partners, "
            "and RCM Private Markets Fund managed by Manager Capital.")
    result = recover(text)
    by_id = {row["entity_id"]: row["name"] for row in result["entities"]}
    assert {by_id[row["subject_id"]] for row in result["claims"]} == {
        "Atlas Ventures", "Beacon Capital", "Birch Partners", "RCM Private Markets Fund"}
    assert all(row["object_id"] == stable_id("ORG", "acme") for row in result["claims"])
    assert "Manager Capital" not in by_id.values()
    for row in result["claims"]:
        assert text[row["evidence_start"]:row["evidence_end"]] == row["evidence"]
        assert "Acme" in row["evidence"] and by_id[row["subject_id"]] in row["evidence"]
    assert len(result["mentions"]) == len({row["mention_id"] for row in result["mentions"]})


def test_ambiguous_recipient_and_speculation_are_not_linked():
    text = "Acme and Globex raised $30 million in a Series B round. The round was led by Atlas Ventures."
    assert not recover(text, ("Acme", "Globex"))["claims"]
    text = "Acme reportedly raised $30 million in a Series B round. The round was led by Atlas Ventures."
    assert not recover(text)["claims"]


def test_reference_cannot_drift_to_another_round_or_unnamed_investor_type():
    text = ("Acme raised $30 million in a Series B round. "
            "Globex raised $20 million in a Series C round. "
            "The round was led by Atlas Ventures and Alex Smith.")
    result = recover(text, ("Acme", "Globex"))
    assert len(result["claims"]) == 1
    assert result["claims"][0]["object_id"] == stable_id("ORG", "globex")
    assert all(row["name"] != "Alex Smith" for row in result["entities"])


def test_reference_window_is_bounded():
    text = ("Acme raised $30 million in a Series B round. " + "The service improved. " * 5
            + "The round was led by Atlas Ventures.")
    assert not recover(text)["claims"]


def test_inline_round_keeps_original_sentence_and_explicit_participants():
    text = ("Acme raised $30 million in a Series B round led by Atlas Ventures "
            "with participation from Beacon Capital and Birch Partners.")
    result = recover(text)
    assert len(result["claims"]) == 3
    assert result["sentences"] == []
    assert all(row["evidence"] == text for row in result["claims"])


def test_two_rounds_in_one_sentence_are_not_guessed():
    text = ("Acme raised $30 million in a Series B round, while Globex raised $20 million "
            "in a Series C round led by Atlas Ventures.")
    assert not recover(text, ("Acme", "Globex"))["claims"]


def test_parent_company_is_not_confused_with_its_named_subsidiary_raising_funds():
    text = ("Acme, a subsidiary of Globex, raised $30 million in a Series B round. "
            "The round was led by Atlas Ventures.")
    result = recover(text, ("Acme", "Globex"))
    assert len(result["claims"]) == 1
    assert result["claims"][0]["object_id"] == stable_id("ORG", "acme")
