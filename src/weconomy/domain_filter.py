"""Evidence-based entity subtypes for the international-business graph."""
import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

from .nlp import normalize, sentences
from .schema import stable_id

VERSION = "initial-domain-v5"
_CUES = {
    "STARTUP": re.compile(r"\b(?:start[- ]?ups?|startup company|công ty khởi nghiệp|doanh nghiệp khởi nghiệp)\b", re.I),
    "VC_FUND": re.compile(r"\b(?:venture capital|VC fund|quỹ đầu tư mạo hiểm|quỹ VC)\b", re.I),
    "INVESTMENT_FUND": re.compile(r"\b(?:investment funds?|quỹ đầu tư)\b", re.I),
    "MULTINATIONAL_CORPORATION": re.compile(
        r"\b(?:multinational (?:company|corporation|group)?|transnational corporation|"
        r"tập đoàn đa quốc gia|doanh nghiệp đa quốc gia)\b", re.I
    ),
    "TECH_COMPANY": re.compile(
        r"\b(?:technology company|tech company|tech firm|technology firm|tech giant|"
        r"công ty công nghệ|tập đoàn công nghệ)\b", re.I
    ),
    "FINANCE_COMPANY": re.compile(
        r"\b(?:financial services company|financial institution|investment bank|fintech company|"
        r"công ty tài chính|tổ chức tài chính|ngân hàng)\b", re.I
    ),
    "BILLIONAIRE": re.compile(r"\b(?:billionaires?|tỷ phú)\b", re.I),
}
_GENERIC_ALIASES = {
    "company", "companies", "fund", "funds", "growth", "investment", "investments",
    "venture", "ventures", "capital", "firm", "firms", "group", "bank", "banks",
    "công ty", "doanh nghiệp", "quỹ", "tập đoàn", "ngân hàng", "cổ phiếu", "usd",
    "ai", "he", "she", "they", "it", "other billionaires", "viable startup",
    "early-stage AI startups", "startup ecosystem", "global startup ecosystem",
    "startup battlefield", "startup battlefield 200", "startup", "startups",
    "venture capital", "the startup", "các", "đây", "nhà", "điều", "việc",
    "tính", "kể", "cam kết", "âu", "his", "ceo", "khoản", "sessions",
    "breakout sessions", "disrupt", "conversation", "cybersecurity",
    "hàn quốc", "trung quốc", "việt nam", "united states", "china", "south korea",
    "disruptive", "tech", "school", "product", "building", "model", "team",
    "techcrunch", "techcrunch disrupt", "techcrunch startup battlefield",
    "or", "three", "number", "innovation", "technology", "chatbot", "market",
    "ecosystem", "engine", "software", "community", "vehicle", "offer", "watch",
    "teams", "breakouts", "something", "stage", "avatar", "app-building", "pitches",
    "program", "commerce", "competition", "discovery", "fintech", "aum", "mac",
    "scaling", "defense", "build", "both", "our", "this", "some", "được", "20",
    "nhật bản", "japan", "năm 2025", "next generation", "semiconductors",
}
_ALLOWED_TYPES = {
    "STARTUP": {"ORG"}, "VC_FUND": {"ORG"}, "INVESTMENT_FUND": {"ORG"},
    "MULTINATIONAL_CORPORATION": {"ORG"}, "TECH_COMPANY": {"ORG"},
    "FINANCE_COMPANY": {"ORG"}, "BILLIONAIRE": {"PERSON"},
}
_APPOSITION_WORDS = {"a", "an", "the", "of", "named", "called", "firm", "company", "group",
                     "là", "một", "nhà", "hãng", "tập", "đoàn", "công", "ty", "quỹ", "đầu",
                     "tư", "tổ", "chức", "tài", "chính", "nghệ", "quốc", "gia", "tỷ", "phú"}


def _mentions(text, pattern):
    return list(pattern.finditer(text))


def _distance(left, right):
    return max(0, max(left[0], right[0]) - min(left[1], right[1]))


def _nearby_words(text, mention, cue):
    gap = text[min(mention[1], cue[1]):max(mention[0], cue[0])]
    return re.findall(r"[\wÀ-ỹ]+", gap.casefold())


def _write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n" for row in rows),
                    encoding="utf-8")


def filter_domain_export(source: Path, output: Path, *, aliases_path=Path("config/entities.yaml")) -> dict:
    """Create a filtered export; original collection/export remains untouched."""
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError(output)
    names = ("articles", "entities", "relations", "claims")
    files = {name: source / f"{name}.jsonl" for name in names}
    if any(not path.is_file() for path in files.values()) or not (source / "manifest.json").is_file():
        raise ValueError("Source must be a complete export-dataset directory")
    rows = {name: [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]
            for name, path in files.items()}
    manifest = json.loads((source / "manifest.json").read_text("utf-8"))
    types = {row["entity_id"]: row["entity_type"] for row in rows["entities"]}
    aliases = defaultdict(set)
    for row in yaml.safe_load(Path(aliases_path).read_text(encoding="utf-8")):
        entity_id = stable_id(row["type"], normalize(row["name"]).casefold())
        if entity_id in types:
            for name in [row["name"], *row.get("aliases", [])]:
                aliases[entity_id].add(normalize(name))
    for entity in rows["entities"]:
        aliases[entity["entity_id"]].add(normalize(entity["name"]))
    alias_ids = defaultdict(set)
    for entity_id, values in aliases.items():
        for value in values:
            if len(value) >= 2 and value.casefold() not in _GENERIC_ALIASES:
                alias_ids[value.casefold()].add(entity_id)
    alias_ids = {alias: ids for alias, ids in alias_ids.items() if len(ids) == 1}
    ordered = sorted(alias_ids, key=len, reverse=True)
    if not ordered:
        raise ValueError("Source export has no classifiable entities")
    mention_re = re.compile(r"(?<!\w)(?P<name>" + "|".join(re.escape(name) for name in ordered) + r")(?!\w)", re.I)

    tags, evidence, tagged_documents, sectors_by_document = (
        defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set))
    for article in rows["articles"]:
        for sentence in sentences(article.get("text", "")):
            text = sentence["text"]
            mentions = []
            for mention in _mentions(text, mention_re):
                for entity_id in alias_ids[normalize(mention.group("name")).casefold()]:
                    mentions.append((mention.start(), mention.end(), entity_id))
                    if types[entity_id] == "GOV":
                        tags[entity_id].add("GOVERNMENT")
                        evidence[entity_id].add(f"{article['document_id']}:curated_entity_type:GOV")
                        tagged_documents[entity_id].add(article["document_id"])
            for domain_type, cue in _CUES.items():
                for match in cue.finditer(text):
                    candidates = [( _distance((start, end), match.span()), entity_id)
                                 for start, end, entity_id in mentions
                                 if types[entity_id] in _ALLOWED_TYPES[domain_type]]
                    if not candidates:
                        continue
                    distance, entity_id = min(candidates)
                    mention_span = next(((start, end) for start, end, candidate_id in mentions
                                         if candidate_id == entity_id and _distance((start, end), match.span()) == distance), None)
                    gap_words = (_nearby_words(text, mention_span, match.span())
                                 if mention_span is not None else [])
                    if (distance > 40 or mention_span is None or len(gap_words) > 2
                            or any(word not in _APPOSITION_WORDS for word in gap_words)):
                        continue
                    if mention_span[0] < match.end() and match.start() < mention_span[1]:
                        continue
                    tags[entity_id].add(domain_type)
                    evidence[entity_id].add(
                        f"{article['document_id']}:{domain_type}:{text[:240]}")
                    tagged_documents[entity_id].add(article["document_id"])
                    if domain_type in {"TECH_COMPANY", "FINANCE_COMPANY"}:
                        sectors_by_document[(article["document_id"], entity_id)].add(domain_type)

    for claim in rows["claims"]:
        if (claim.get("predicate") == "CEO_OF"
                and types.get(claim.get("subject_id")) == "PERSON"
                and sectors_by_document.get((claim.get("document_id"), claim.get("object_id")))):
            tags[claim["subject_id"]].add("TECH_FINANCE_CEO")
            evidence[claim["subject_id"]].add(f"{claim['document_id']}:{claim['evidence'][:240]}")
            tagged_documents[claim["subject_id"]].add(claim["document_id"])

    tagged = {entity_id: sorted(values) for entity_id, values in tags.items() if values}
    eligible = set(tagged)
    claims = [row for row in rows["claims"]
              if row["subject_id"] in eligible and row["object_id"] in eligible]
    typed_entities = [{**entity, "domain_types": tagged[entity["entity_id"]],
                       "domain_evidence": sorted(evidence[entity["entity_id"]])[:5]}
                      for entity in rows["entities"] if entity["entity_id"] in eligible]
    article_ids = {document_id for entity_id in eligible for document_id in tagged_documents[entity_id]}
    article_ids.update(row["document_id"] for row in claims)
    articles = [row for row in rows["articles"] if row["document_id"] in article_ids]
    triples = {}
    for row in rows["relations"]:
        if row["subject_id"] in eligible and row["object_id"] in eligible:
            triples.setdefault((row["subject_id"], row["predicate"], row["object_id"]), row)

    counts = {"articles": len(articles), "nodes": len(typed_entities), "relations": len(triples),
              "claims": len(claims), "relation_types": len({row["predicate"] for row in claims})}
    status = manifest.get("status", {})
    if isinstance(status, dict):
        status = {**status, "counts": counts, "reason": "domain_filtered",
                  "targets_met": all(counts.get(key, 0) >= value for key, value in status.get("targets", {}).items()
                                     if value is not None)}
    filtered_manifest = {**manifest, "status": status, "counts": counts,
                         "quality": {**manifest.get("quality", {}),
                                     "domain_filter": VERSION,
                                     "precision": None},
                         "domain_filter": {"version": VERSION, "types": sorted(
                             {kind for entity in typed_entities for kind in entity["domain_types"]}),
                             "excluded_entities": len(rows["entities"]) - len(typed_entities),
                             "excluded_claims": len(rows["claims"]) - len(claims)}}
    output.mkdir(parents=True)
    _write_jsonl(output / "articles.jsonl", articles)
    _write_jsonl(output / "entities.jsonl", typed_entities)
    _write_jsonl(output / "relations.jsonl", list(triples.values()))
    _write_jsonl(output / "claims.jsonl", claims)
    (output / "manifest.json").write_text(
        json.dumps(filtered_manifest, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    return {"output": str(output), "counts": counts, "domain_filter": filtered_manifest["domain_filter"]}
