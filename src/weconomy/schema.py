"""Explicit Arrow types keep empty runs and downstream readers compatible."""
import hashlib
import json

import pyarrow as pa

SCHEMA_VERSION = "1.1"


def stable_id(*parts: str) -> str:
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False).encode()).hexdigest()[:24]


def schema(fields):
    return pa.schema([(name, typ) for name, typ in fields], metadata={b"version": SCHEMA_VERSION.encode()})


S = pa.string()
INT = pa.int64()
SCHEMAS = {
    "bronze": schema([(x, S) for x in (
        "document_id", "url", "source_id", "kind", "attribution", "retrieved_at",
        "published_at", "language_hint", "raw_html", "raw_sha256", "response_headers", "capture_scope",
        "raw_path", "discovery_endpoint"
    )] + [("raw_bytes", pa.binary())]),
    "articles": schema([(x, S) for x in (
        "document_id", "title", "text", "language", "routing_method", "content_sha256", "duplicate_of",
        "content_status", "extraction_method", "extractor_version", "published_at", "authors",
        "quality_flags", "canonical_url"
    )] + [("word_count", INT), ("body_paragraphs", INT), ("trafilatura_coverage", pa.float64()),
          ("paragraph_coverage", pa.float64()), ("nlp_eligible", pa.bool_())]),
    "sentences": schema([("sentence_id", S), ("document_id", S), ("text", S), ("start", INT), ("end", INT)]),
    "mentions": schema([(x, S) for x in ("mention_id", "document_id", "sentence_id", "entity_id", "surface",
                                        "entity_type", "method")] + [("start", INT), ("end", INT)]),
    "entities": schema([(x, S) for x in ("entity_id", "name", "entity_type", "resolution_method")]),
    "relations": schema([(x, S) for x in (
        "claim_id", "event_id", "subject_id", "predicate", "object_id", "document_id", "sentence_id",
        "evidence", "trigger", "rule_id", "assertion_status", "review_status", "event_date"
    )] + [("evidence_start", INT), ("evidence_end", INT)]),
    "events": schema([(x, S) for x in (
        "event_id", "subject_id", "predicate", "object_id", "assertion_status", "event_date", "dedup_scope"
    )]),
}

# Optional endpoint-type constraints for domain relation predicates; other labels remain supported.
RELATION_TYPES = {
    "ACQUIRED": (["ORG"], ["ORG"]),
    "AGREED_TO_ACQUIRE": (["ORG"], ["ORG"]),
    "INVESTED_IN": (["ORG", "PERSON"], ["ORG"]),
    "MERGED_WITH": (["ORG"], ["ORG"]),
    "SUED": (["ORG", "PERSON", "GOV"], ["ORG", "PERSON"]),
    "PARTNERED_WITH": (["ORG"], ["ORG"]),
    "SUPPLIES_TO": (["ORG"], ["ORG"]),
    "CEO_OF": (["PERSON"], ["ORG"]),
    "FOUNDED": (["PERSON", "ORG"], ["ORG"]),
    "SUBSIDIARY_OF": (["ORG"], ["ORG"]),
    "REGULATES": (["GOV"], ["ORG"]),
    "OWNS_STAKE_IN": (["PERSON", "ORG"], ["ORG"]),
    "BOARD_MEMBER_OF": (["PERSON"], ["ORG"]),
    "CONTRACTED_WITH": (["ORG"], ["ORG"]),
    "AWARDED_CONTRACT_TO": (["GOV", "ORG"], ["ORG"]),
    "ANTITRUST_ACTION_AGAINST": (["GOV"], ["ORG"]),
    "SANCTIONED": (["GOV"], ["ORG", "PERSON"]),
    "DISRUPTED_SUPPLY_TO": (["GOV", "ORG"], ["ORG"]),
    "SPUN_OFF_FROM": (["ORG"], ["ORG"]),
    "INVESTIGATES": (["GOV"], ["ORG", "PERSON"]),
    "CLOSED_INVESTIGATION_INTO": (["GOV"], ["ORG", "PERSON"]),
    "LICENSED_TECH_FROM": (["ORG"], ["ORG"]),
}

SYMMETRIC_RELATIONS = frozenset({
    "CO_INVESTED_WITH", "CO_FINANCED_WITH", "COMPETES_WITH", "MERGED_WITH", "PARTNERED_WITH",
})
