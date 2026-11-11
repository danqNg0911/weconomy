"""TEST_ONLY strings exercise routing; they are not collected news."""

from weconomy.domain import DOMAIN_VERSION, classify


def test_english_ceo_and_merger():
    result = classify("TEST_ONLY: CEO merger", "A company completes an acquisition", "en")
    assert result["in_scope"] and "executive_or_founder" in result["reasons"]


def test_fund_investment():
    result = classify("TEST_ONLY: Fund investment", "A firm invests in a startup", "en")
    assert "corporate_actor_transaction" in result["reasons"]


def test_corporate_investment_verb_without_title_cue():
    result = classify("TEST_ONLY: Investment", "A company invests in a startup", "en")
    assert "corporate_actor_transaction" in result["reasons"]


def test_government_antitrust():
    result = classify("TEST_ONLY: Antitrust review", "Government reviews competition law", "en")
    assert result["in_scope"] and "antitrust" in result["reasons"]


def test_domestic_startup_needs_no_country_cue():
    assert classify("TEST_ONLY: Startup", "A local startup opens", "en")["in_scope"]


def test_vietnamese_accents_and_case():
    result = classify("TEST_ONLY: CHUỖI CUNG ỨNG", "Tập đoàn", "vi")
    assert "supply_chain" in result["reasons"]
    assert "corporate_actor_transaction" in result["reasons"]


def test_english_sports_is_excluded():
    assert not classify("TEST_ONLY: Football final", "Team wins the match", "en")["in_scope"]


def test_local_road_budget_is_excluded():
    result = classify("TEST_ONLY: Road budget", "Local public investment funds housing", "en")
    assert not result["in_scope"]


def test_empty_input_and_frozen_scope():
    result = classify("", "", "")
    assert result == {"in_scope": False, "reasons": [], "scope": DOMAIN_VERSION}
