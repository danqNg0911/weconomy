import json
from pathlib import Path

import yaml

from weconomy.domain_filter import VERSION, _generic_alias, filter_domain_export
from weconomy.schema import stable_id


def _write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                    encoding="utf-8")


def test_filter_domain_rejects_generic_mentions_and_accepts_expanded_cues(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    document_id = "article-1"
    text = ("Anthropic is an AI company. Sequoia is a venture firm. "
            "Nvidia is a semiconductor company. Acme is a fintech startup. "
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
        ("Russia", "ORG"), ("Canada", "GOV"),
    ]
    entities = [{"entity_id": stable_id(kind, name.casefold()), "name": name, "entity_type": kind}
                for name, kind in names]
    entity_ids = {entity["name"]: entity["entity_id"] for entity in entities}
    claims = [
        {"document_id": document_id, "subject_id": entity_ids["Anthropic"],
         "predicate": "PARTNERED_WITH", "object_id": entity_ids["Sequoia"],
         "evidence": "Anthropic partnered with Sequoia."},
        {"document_id": document_id, "subject_id": entity_ids["the company"],
         "predicate": "INVESTED_IN", "object_id": entity_ids["Nvidia"],
         "evidence": "The company invested in Nvidia."},
    ]
    _write_jsonl(source / "articles.jsonl", [
        {"document_id": document_id, "text": text},
    ])
    _write_jsonl(source / "entities.jsonl", entities)
    _write_jsonl(source / "claims.jsonl", claims)
    _write_jsonl(source / "relations.jsonl", [
        {key: row[key] for key in ("subject_id", "predicate", "object_id")} for row in claims
    ])
    (source / "manifest.json").write_text(json.dumps({"status": {"targets": {}}}), encoding="utf-8")
    aliases = tmp_path / "aliases.yaml"
    aliases.write_text(yaml.safe_dump([{"name": "United States", "type": "GOV", "aliases": ["US"]}]),
                      encoding="utf-8")

    result = filter_domain_export(source, tmp_path / "filtered", aliases_path=aliases)

    filtered_entities = [json.loads(line) for line in (tmp_path / "filtered/entities.jsonl").read_text(
        encoding="utf-8").splitlines()]
    filtered_claims = [json.loads(line) for line in (tmp_path / "filtered/claims.jsonl").read_text(
        encoding="utf-8").splitlines()]
    by_name = {entity["name"]: entity for entity in filtered_entities}
    assert VERSION == "initial-domain-v8"
    assert by_name["Anthropic"]["domain_types"] == ["TECH_COMPANY"]
    assert by_name["Sequoia"]["domain_types"] == ["VC_FUND"]
    assert by_name["Nvidia"]["domain_types"] == ["TECH_COMPANY"]
    assert "STARTUP" in by_name["Acme"]["domain_types"]
    assert by_name["Michael Tan"]["domain_types"] == ["BILLIONAIRE"]
    assert by_name["United States"]["domain_types"] == ["GOVERNMENT"]
    assert not {"AI", "startup", "the company", "2024", "consumer", "AI chip", "hardware",
                "early-stage", "Expo Hall", "Third", "chip", "products", "Bitcoin"}.intersection(by_name)
    assert "SpaceX" not in by_name
    assert "STARTUP" in by_name["Tenstorrent"]["domain_types"]
    assert "TECH_COMPANY" in by_name["Anterior"]["domain_types"]
    assert not {"OECD", "California", "WHO"}.intersection(by_name)
    assert by_name["Canada"]["domain_types"] == ["GOVERNMENT"]
    assert "Russia" not in by_name
    assert _generic_alias("Trung Quốc Central Huijin hiện")
    assert len(filtered_claims) == 1
    assert result["counts"]["relations"] == 1
