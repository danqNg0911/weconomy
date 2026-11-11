import json

import pytest
import yaml

from weconomy.domain_filter import VERSION, _generic_alias, filter_domain_export
from weconomy.schema import stable_id


def _write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                    encoding="utf-8")


def test_filter_domain_rejects_generic_mentions_and_accepts_curated_entities(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    document_id = "article-1"
    text = ("Anthropic is an AI company. Sequoia is a venture firm. "
            "Anthropic partnered with Sequoia. "
            "Nvidia is a semiconductor company. Acme is a fintech startup. "
            "The report mentions new fundraising and Its in a sentence. "
            "The report discussed work the startup completed. "
            "Globex reported gains. OneTimeCo launched a service. "
            "Michael Tan is a billionaire. The United States government acted. "
            "The company launched in 2024; AI and consumer were mentioned. "
            "AI hardware startups are growing. The total included an early-stage venture fund. "
            "Find an opportunity in the Expo Hall, the Startup Battlefield. "
            "Tenstorrent, a chip startup, raised funding. Fidelity invested in SpaceX; "
            "the Saudi sovereign wealth fund invested too. "
            "Anterior is a healthcare AI company. According to the OECD, AI companies grew. "
            "The hospital systems in California, a bank in Rhode Island, were affected. "
            "Batroukh is joined by founder Omar Shakir, who is its startup CTO. "
            "Russia is a financial institution. Canada government acted.")
    names = [
        ("Anthropic", "ORG"), ("AI", "ORG"), ("Sequoia", "ORG"),
        ("Nvidia", "ORG"), ("Acme", "ORG"), ("startup", "ORG"),
        ("the company", "ORG"), ("2024", "ORG"), ("consumer", "ORG"),
        ("AI chip", "ORG"), ("hardware", "ORG"), ("early-stage", "ORG"),
        ("Expo Hall", "ORG"), ("Third", "ORG"), ("chip", "ORG"),
        ("products", "ORG"), ("Bitcoin", "ORG"),
        ("SpaceX", "ORG"), ("Tenstorrent", "ORG"), ("Anterior", "ORG"),
        ("OECD", "ORG"), ("California", "ORG"), ("WHO", "ORG"),
        ("Michael Tan", "PERSON"), ("United States", "GOV"),
        ("Russia", "ORG"), ("Canada", "GOV"), ("new fundraising", "ORG"),
        ("Its", "ORG"), ("he", "PERSON"), ("work", "ORG"),
        ("Globex", "ORG"), ("OneTimeCo", "ORG"),
    ]
    entities = [{"entity_id": stable_id(kind, name.casefold()), "name": name, "entity_type": kind}
                for name, kind in names]
    entity_ids = {entity["name"]: entity["entity_id"] for entity in entities}
    event_id = stable_id(entity_ids["Anthropic"], "PARTNERED_WITH", entity_ids["Sequoia"],
                         "reported", document_id)
    evidence = "Anthropic partnered with Sequoia."
    canonical_claim_id = stable_id(event_id, stable_id(document_id, str(text.index(evidence)), evidence))
    claims = [
        {"document_id": document_id, "sentence_id": "sentence-1", "subject_id": entity_ids["Anthropic"],
         "predicate": "PARTNERED_WITH", "object_id": entity_ids["Sequoia"],
         "assertion_status": "reported", "event_id": event_id, "claim_id": canonical_claim_id,
         "evidence": "Anthropic partnered with Sequoia."},
        {"document_id": document_id, "sentence_id": "sentence-1", "subject_id": entity_ids["Anthropic"],
         "predicate": "PARTNERED_WITH", "object_id": entity_ids["Sequoia"],
         "assertion_status": "reported", "event_id": "stale-event", "claim_id": "stale-claim",
         "evidence": "Anthropic partnered with Sequoia."},
        {"document_id": document_id, "subject_id": entity_ids["the company"],
         "predicate": "INVESTED_IN", "object_id": entity_ids["Nvidia"],
         "evidence": "The company invested in Nvidia."},
        {"document_id": document_id, "sentence_id": "sentence-2", "subject_id": entity_ids["he"],
         "predicate": "CEO_OF", "object_id": entity_ids["Anthropic"],
         "assertion_status": "reported", "event_id": "pronoun-event", "claim_id": "pronoun-claim",
         "evidence": "He is CEO of Anthropic."},
    ]
    _write_jsonl(source / "articles.jsonl", [
        {"document_id": document_id, "text": text},
        {"document_id": "article-2", "text": "Globex expanded its services."},
    ])
    _write_jsonl(source / "entities.jsonl", entities)
    _write_jsonl(source / "claims.jsonl", claims)
    _write_jsonl(source / "relations.jsonl", [
        {key: row[key] for key in ("subject_id", "predicate", "object_id")} for row in claims
    ])
    (source / "manifest.json").write_text(json.dumps({"status": {"targets": {}}}), encoding="utf-8")
    aliases = tmp_path / "aliases.yaml"
    aliases.write_text(yaml.safe_dump([
        {"name": "United States", "type": "GOV", "aliases": ["US"]},
        {"name": "SpaceX", "type": "ORG", "aliases": []},
    ]), encoding="utf-8")

    result = filter_domain_export(source, tmp_path / "filtered", aliases_path=aliases)

    filtered_entities = [json.loads(line) for line in (tmp_path / "filtered/entities.jsonl").read_text(
        encoding="utf-8").splitlines()]
    filtered_claims = [json.loads(line) for line in (tmp_path / "filtered/claims.jsonl").read_text(
        encoding="utf-8").splitlines()]
    audit_entities = [json.loads(line) for line in (tmp_path / "filtered/audit/entities.jsonl").read_text(
        encoding="utf-8").splitlines()]
    by_name = {entity["name"]: entity for entity in audit_entities}
    accepted_names = {entity["name"] for entity in filtered_entities}
    assert VERSION == "initial-domain-v20-regulatory-verified"
    assert set(by_name["Anthropic"]["domain_types"]) == {
        "BUSINESS_ORGANIZATION", "BUSINESS_COUNTERPARTY", "TECH_COMPANY"}
    assert set(by_name["Sequoia"]["domain_types"]) == {
        "BUSINESS_ORGANIZATION", "BUSINESS_COUNTERPARTY", "VC_FUND"}
    assert by_name["Nvidia"]["domain_types"] == ["BUSINESS_ORGANIZATION", "TECH_COMPANY"]
    assert by_name["Acme"]["domain_types"] == ["BUSINESS_ORGANIZATION", "STARTUP", "TECH_COMPANY"]
    assert by_name["Michael Tan"]["domain_types"] == ["BILLIONAIRE"]
    assert by_name["United States"]["domain_types"] == ["GOVERNMENT"]
    assert not {"AI", "startup", "the company", "2024", "consumer", "AI chip", "hardware",
                "early-stage", "Expo Hall", "Third", "chip", "products", "Bitcoin"}.intersection(accepted_names)
    assert by_name["SpaceX"]["domain_types"] == ["BUSINESS_ORGANIZATION"]
    assert by_name["Globex"]["domain_types"] == []
    assert not {"California", "OECD", "WHO", "new fundraising", "Its", "he", "work", "OneTimeCo"}.intersection(accepted_names)
    assert by_name["Tenstorrent"]["domain_types"] == ["BUSINESS_ORGANIZATION", "STARTUP", "TECH_COMPANY"]
    assert by_name["Anterior"]["domain_types"] == ["BUSINESS_ORGANIZATION", "TECH_COMPANY"]
    assert by_name["Canada"]["domain_types"] == ["GOVERNMENT"]
    assert not by_name["Russia"]["domain_types"]
    assert all(_generic_alias(name) for name in
               ("partnership", "bot", "stories", "communities", "winner", "networking",
                "the companies", "security", "further"))
    assert _generic_alias("Trung Quốc Central Huijin hiện")
    assert len(filtered_claims) == 1
    assert filtered_claims[0]["claim_id"] == canonical_claim_id
    assert filtered_claims[0]["event_id"] == event_id
    assert result["counts"]["relations"] == 1
    assert result["counts"]["articles"] == 1
    assert result["counts"]["nodes"] == 2
    assert accepted_names == {"Anthropic", "Sequoia"}


def test_verification_canonicalizes_named_heads_and_exports_only_evidenced_claims(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    names = ["Meta", "AI agent startup Manus", "Manus", "Series H"]
    ids = {name: stable_id("ORG", name.casefold()) for name in names}
    text = "Meta is a technology company. Meta acquired AI agent startup Manus."
    _write_jsonl(source / "articles.jsonl", [{"document_id": "doc", "language": "en", "text": text}])
    _write_jsonl(source / "entities.jsonl", [
        {"entity_id": ids[name], "name": name, "entity_type": "ORG"} for name in names])
    claims = [{"document_id": "doc", "sentence_id": "sid", "subject_id": ids["Meta"],
               "object_id": ids[name], "predicate": "ACQUIRED", "assertion_status": "reported",
               "evidence": "Meta acquired AI agent startup Manus."}
              for name in ("AI agent startup Manus", "Manus")]
    claims.append(dict(claims[0], sentence_id="false", evidence="Meta acquired Manus.", claim_id="false"))
    _write_jsonl(source / "claims.jsonl", claims)
    _write_jsonl(source / "relations.jsonl", [dict(claims[0], predicate="MERGED_WITH")])
    (source / "manifest.json").write_text("{}", encoding="utf-8")
    aliases = tmp_path / "aliases.yaml"
    aliases.write_text("[]", encoding="utf-8")
    result = filter_domain_export(source, tmp_path / "verified", aliases_path=aliases)
    entities = [json.loads(row) for row in (tmp_path / "verified/entities.jsonl").read_text("utf-8").splitlines()]
    edges = [json.loads(row) for row in (tmp_path / "verified/relations.jsonl").read_text("utf-8").splitlines()]
    assert {row["name"] for row in entities} == {"Meta", "Manus"}
    assert [(row["subject_id"], row["predicate"], row["object_id"]) for row in edges] == [
        (ids["Meta"], "ACQUIRED", ids["Manus"])]
    assert result["counts"]["nodes"] == 2
    assert result["counts"]["claims"] == 1
    assert result["domain_filter"]["merged_entities"] == 1
    assert result["domain_filter"]["claim_reasons"]["evidence_not_in_article"] == 1


def test_normalize_recovers_explicit_round_evidence_without_model_calls(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    text = ("Acme, a London-based robotics startup, has raised $30 million in a Series B round. "
            "The round was led by Atlas Ventures. Other investors in this round include Beacon Capital.")
    _write_jsonl(source / "articles.jsonl", [{"document_id": "doc", "language": "en", "text": text}])
    _write_jsonl(source / "entities.jsonl", [{"entity_id": stable_id("ORG", "acme"),
                                            "name": "Acme", "entity_type": "ORG"}])
    for kind in ("claims", "relations"):
        _write_jsonl(source / f"{kind}.jsonl", [])
    (source / "manifest.json").write_text("{}", encoding="utf-8")
    aliases = tmp_path / "aliases.yaml"
    aliases.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("weconomy.nlp.NLP.__init__", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no NLP")))
    result = filter_domain_export(source, tmp_path / "verified", aliases_path=aliases)
    assert result["counts"]["nodes"] == 3
    assert result["counts"]["relations"] == 2
    assert result["domain_filter"]["derived_entities"] == 2
    entities = [json.loads(row) for row in (tmp_path / "verified/entities.jsonl").read_text("utf-8").splitlines()]
    assert {row["name"] for row in entities} == {"Acme", "Atlas Ventures", "Beacon Capital"}


def test_document_spans_do_not_confuse_same_name_types_across_articles(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    company, person, fund = stable_id("ORG", "acme"), stable_id("PERSON", "acme"), stable_id("ORG", "atlas ventures")
    text = "Acme is a startup. Atlas Ventures invested in Acme."
    _write_jsonl(source / "articles.jsonl", [{"document_id": "doc", "language": "en", "text": text},
                                            {"document_id": "other", "language": "en", "text": "Acme spoke."}])
    _write_jsonl(source / "entities.jsonl", [{"entity_id": company, "name": "Acme", "entity_type": "ORG"},
                                            {"entity_id": person, "name": "Acme", "entity_type": "PERSON"},
                                            {"entity_id": fund, "name": "Atlas Ventures", "entity_type": "ORG"}])
    _write_jsonl(source / "mentions.jsonl", [
        {"document_id": "doc", "entity_id": entity_id, "surface": surface,
         "start": start, "end": start + len(surface)} for entity_id, surface, start in [
             (company, "Acme", 0), (fund, "Atlas Ventures", text.index("Atlas Ventures")),
             (company, "Acme", text.rindex("Acme"))]])
    _write_jsonl(source / "claims.jsonl", [{"document_id": "doc", "sentence_id": "sid", "subject_id": fund,
        "predicate": "INVESTED_IN", "object_id": company, "assertion_status": "reported",
        "evidence": "Atlas Ventures invested in Acme."}])
    _write_jsonl(source / "relations.jsonl", [])
    (source / "manifest.json").write_text("{}", encoding="utf-8")
    aliases = tmp_path / "aliases.yaml"
    aliases.write_text("[]", encoding="utf-8")
    result = filter_domain_export(source, tmp_path / "verified", aliases_path=aliases)
    assert result["counts"]["nodes"] == 2
    assert result["counts"]["relations"] == 1


@pytest.mark.parametrize("description,short,full,expected", [
    ("Fusion startup Inertia Enterprises announced a product.", "Inertia", "Inertia Enterprises", True),
    ("Inertia Enterprises announced a product.", "Inertia", "Inertia Enterprises", True),
    ("Redwood Materials announced a product.", "Redwood", "Redwood Materials", True),
    ("Valar Atomics, a nuclear startup, announced a product.", "Valar", "Valar Atomics", True),
    ("Salesforce Foundation, a startup, announced a product.", "Salesforce", "Salesforce Foundation", False),
])
def test_document_name_expansion_preserves_evidence_and_does_not_merge_foundations(
        tmp_path, description, short, full, expected):
    result, output = _context_export(tmp_path, description + f" Jane Doe, CEO of {short}, spoke.",
                                     [(full, "ORG"), (short, "ORG"), ("Jane Doe", "PERSON")])
    claims = [json.loads(line) for line in (output / "claims.jsonl").read_text("utf-8").splitlines()]
    assert bool(result["counts"]["relations"]) is expected
    if expected:
        assert {row["object_id"] for row in claims} == {stable_id("ORG", full.casefold())}
        assert all(short in row["evidence"] for row in claims)


@pytest.mark.parametrize("text,expected", [
    ("Acme announced a product. The company is a robotics startup. Jane Doe, CEO of Acme, spoke.", True),
    ("Acme and Globex announced a product. The company is a robotics startup. Jane Doe, CEO of Acme, spoke.", False),
    ("Acme announced a product.\n\nThe company is a robotics startup. Jane Doe, CEO of Acme, spoke.", False),
    ("Acme discussed a startup. Jane Doe, CEO of Acme, spoke.", False),
    ("Acme announced a product. The company invested in a robotics startup. Jane Doe, CEO of Acme, spoke.", False),
])
def test_adjacent_reference_requires_one_organization_and_explicit_description(tmp_path, text, expected):
    result, _ = _context_export(tmp_path, text, [("Acme", "ORG"), ("Globex", "ORG"), ("Jane Doe", "PERSON")])
    assert bool(result["counts"]["relations"]) is expected


def test_name_expansion_abstains_on_ambiguous_corporate_names():
    from weconomy.entity_quality import organization_name_aliases

    names = {"short": "Acme", "one": "Acme Health", "two": "Acme Technologies"}
    assert not organization_name_aliases([(0, 4, key) for key in names], names)
    assert not organization_name_aliases([(0, 4, "short")], names)


def test_vietnamese_explicit_subsidiary_is_business_evidence(tmp_path):
    result, _ = _context_export(tmp_path,
        "Red River Talc, công ty con của Johnson & Johnson, đưa ra đề xuất.",
        [("Red River Talc", "ORG"), ("Johnson & Johnson", "ORG")], language="vi")
    assert result["counts"]["relations"] == 1


@pytest.mark.parametrize("context,canonical", [
    ("Alphabet’s X moonshot factory acted.", "X (Alphabet)"),
    ("Astro Teller, CEO of X, Alphabet’s “moonshot factory,” spoke.", "X (Alphabet)"),
    ("Musk’s social media company X acted.", "X (social network)"),
    ("X acted.", None),
    ("Alphabet’s X moonshot factory acted. Musk’s social media company X acted.", None),
])
def test_normalize_uses_document_context_before_binding_ambiguous_x(tmp_path, context, canonical):
    result, output = _context_export(tmp_path, context + " Acme is a startup. X partnered with Acme.",
                                     [("X", "ORG"), ("Acme", "ORG")])
    entities = [json.loads(line) for line in (output / "entities.jsonl").read_text("utf-8").splitlines()]
    if canonical:
        assert result["counts"]["relations"] == 1
        assert {row["name"] for row in entities} == {canonical, "Acme"}
        assert any(row["entity_id"] == stable_id("ORG", canonical.casefold()) for row in entities)
    else:
        assert not result["counts"]["relations"]


@pytest.mark.parametrize("context,expected", [("Musk’s social media company X grew. ", True), ("", False)])
def test_funding_recovery_cannot_reintroduce_an_unresolved_global_x(tmp_path, context, expected):
    result, output = _context_export(tmp_path,
        context + "Acme raised $15 million in a Series A round. The round was led by X.",
        [("Acme", "ORG"), ("X", "ORG")])
    entities = [json.loads(line) for line in (output / "entities.jsonl").read_text("utf-8").splitlines()]
    assert bool(result["counts"]["relations"]) is expected
    assert all(row["name"] != "X" for row in entities)


def test_legacy_government_type_and_nested_generic_mentions_do_not_hide_a_closed_case(tmp_path):
    result, output = _context_export(tmp_path,
        "United States Securities and Exchange Commission has closed its investigation into startup Acme.",
        [("Securities and Exchange Commission", "ORG"), ("Commission", "ORG"), ("Acme", "ORG")])
    assert result["counts"]["relations"] == 1
    claims = [json.loads(line) for line in (output / "claims.jsonl").read_text("utf-8").splitlines()]
    assert claims[0]["predicate"] == "CLOSED_INVESTIGATION_INTO"
    entities = [json.loads(line) for line in (output / "entities.jsonl").read_text("utf-8").splitlines()]
    assert any(row["entity_type"] == "GOV" for row in entities)


def test_legacy_country_span_inside_an_official_agency_does_not_steal_its_action(tmp_path):
    text = "United States Securities and Exchange Commission has closed its investigation into startup Acme."
    _context_export(tmp_path, text,
        [("United States Securities and Exchange Commission", "ORG"), ("United States", "GOV"), ("Acme", "ORG")])
    source = tmp_path / "source"
    with (source / "mentions.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"document_id": "doc", "entity_id": stable_id("GOV", "united states"),
                                 "start": 0, "end": 13, "surface": "United States"}) + "\n")
    result = filter_domain_export(source, tmp_path / "overlap-verified", aliases_path=tmp_path / "aliases.yaml")
    assert result["counts"]["relations"] == 1


@pytest.mark.parametrize("role", ["former Acme CEO Jane Doe", "Jane Doe, former CEO of Acme"])
def test_historical_ceo_is_not_exported_as_current_role(tmp_path, role):
    result, output = _context_export(tmp_path, "Acme is a startup. Investors include " + role + ".",
                                     [("Acme", "ORG"), ("Jane Doe", "PERSON")])
    assert not result["counts"]["relations"]
    audit = [json.loads(line) for line in (output / "audit/claims.jsonl").read_text("utf-8").splitlines()]
    assert not audit or any(row["reason"] == "historical_role_requires_temporal_qualification" for row in audit)


def _context_export(tmp_path, text, names, language="en"):
    import re

    source = tmp_path / "source"
    source.mkdir()
    entities = [{"entity_id": stable_id(kind, name.casefold()), "name": name, "entity_type": kind}
                for name, kind in names]
    mentions = []
    for entity in entities:
        for match in re.finditer(r"(?<!\w)" + re.escape(entity["name"]) + r"(?!\w)", text):
            # Record the longest entity at a span, as actual model output does.
            if any(other["name"] != entity["name"] and other["name"].startswith(entity["name"] + " ")
                   and text[match.start():].startswith(other["name"]) for other in entities):
                continue
            mentions.append({"document_id": "doc", "entity_id": entity["entity_id"],
                             "start": match.start(), "end": match.end(), "surface": match.group()})
    _write_jsonl(source / "articles.jsonl", [{"document_id": "doc", "language": language, "text": text}])
    _write_jsonl(source / "entities.jsonl", entities)
    _write_jsonl(source / "mentions.jsonl", mentions)
    for name in ("claims", "relations"):
        _write_jsonl(source / f"{name}.jsonl", [])
    (source / "manifest.json").write_text("{}", encoding="utf-8")
    aliases = tmp_path / "aliases.yaml"
    aliases.write_text("[]", encoding="utf-8")
    output = tmp_path / "verified"
    return filter_domain_export(source, output, aliases_path=aliases), output
