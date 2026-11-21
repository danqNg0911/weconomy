import pytest
from app import graph_rag
from app.config import Settings
from app.guards import normalize
from app.query_normalization import FOLDS, normalize_plan, partial_terms, variants


@pytest.mark.parametrize("name", ["Nhật Bản", "nhat ban", "  JAPAN  "])
def test_country_variants_bilingual_and_accentless(name):
    assert {"nhat ban", "japan"} <= set(variants(name))


def test_aliases_do_not_translate_substrings_or_merge_entities():
    plan = graph_rag.Plan(
        entities=["Mỹ", "United States", "TDK Ventures", "Japan Airlines"], terms=[], relations=[]
    )
    groups = normalize_plan(plan)["entities"]
    assert len(groups) == 3
    assert "united states" in groups[0]["variants"]
    assert groups[1]["variants"] == ["tdk ventures"]
    assert groups[2]["variants"] == ["japan airlines"]


def test_country_aliases_do_not_match_person_name_substrings():
    assert partial_terms(variants("Nhật Bản")) == []
    assert partial_terms(variants("Mỹ")) == []
    assert partial_terms(variants("TDK Ventures")) == ["tdk ventures"]


def test_model_supplied_equivalent_names_and_keyword_fallback():
    plan = graph_rag.Plan(
        entities=["Ngân hàng Trung ương châu Âu"],
        entity_variants={"Ngân hàng Trung ương châu Âu": ["European Central Bank", "ECB"]},
        terms=["đầu tư", "investment"],
        relations=[],
    )
    normalized = normalize_plan(plan)
    assert "european central bank" in normalized["entities"][0]["variants"]
    assert normalized["fallback_terms"] == ["dau tu", "investment"]


def test_cypher_fold_table_matches_vietnamese_normalization():
    text = "ĐẦU TƯ tại Việt Nam, NHẬT BẢN".lower()
    for source, target in FOLDS:
        text = text.replace(source, target)
    assert text == normalize("ĐẦU TƯ tại Việt Nam, NHẬT BẢN")


def test_linking_prefers_exact_and_uses_fallback_only_after_miss():
    class Node(dict):
        element_id = "japan"

    class Transaction:
        def __init__(self):
            self.terms = []

        def run(self, query, **params):
            if query != graph_rag.LINK_QUERY:
                return []
            self.terms.append(params["terms"])
            if "japan" in params["terms"]:
                return [{"n": Node(name="Japan"), "score": 2}, {"n": Node(name="Japan Airlines"), "score": 1}]
            return []

    settings = Settings(_env_file=None)
    tx = Transaction()
    result = graph_rag.traverse(
        tx, settings, graph_rag.Plan(entities=["nhat ban"], terms=["unused"], relations=[])
    )
    assert result["graph"]["nodes"][0]["label"] == "Japan"
    assert len(tx.terms) == 1
    tx = Transaction()
    result = graph_rag.traverse(
        tx, settings, graph_rag.Plan(entities=["Unknown spelling"], terms=["Japan"], relations=[])
    )
    assert len(tx.terms) == 2
    assert result["metadata"]["seed_ids"] == ["japan"]
    assert result["metadata"]["normalization"]["entities"][0]["original"] == "Unknown spelling"
