"""Evidence-based entity subtypes for the international-business graph."""
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.parquet as pq
import yaml

from .entity_quality import (
    entity_name_issue,
    government_aliases,
    historical_role,
    named_head,
    organization_name_aliases,
    x_organization_context,
)
from .funding import funding_references
from .nlp import extract_relations, normalize, sentences, supported_relation
from .schema import RELATION_TYPES, SYMMETRIC_RELATIONS, stable_id

VERSION = "initial-domain-v20-regulatory-verified"
_CUES = {
    "BUSINESS_ORGANIZATION": re.compile(
        r"\b(?:companies|company|firms?|corporations?|conglomerates?|banks?|"
        r"công ty|doanh nghiệp|tập đoàn|ngân hàng)\b", re.I),
    "STARTUP": re.compile(
        r"\b(?:(?:ai|tech(?:nology)?|fintech|software|biotech|deep[- ]tech|chip|hardware|EV)\s+)?"
        r"start[- ]?ups?(?: company)?\b|\b(?:công ty|doanh nghiệp) khởi nghiệp\b", re.I),
    "VC_FUND": re.compile(
        r"\b(?:venture capital(?: firm| fund)?|venture firm|venture fund|VC (?:firm|fund))\b|"
        r"\bquỹ (?:đầu tư mạo hiểm|VC)\b", re.I),
    "INVESTMENT_FUND": re.compile(
        r"\b(?:investment funds?|investment firms?|private equity (?:funds?|firms?)|"
        r"hedge funds?|sovereign wealth funds?|growth equity funds?)\b|"
        r"\bquỹ đầu tư(?: tư nhân| quốc gia)?\b", re.I),
    "MULTINATIONAL_CORPORATION": re.compile(
        r"\b(?:multinational (?:company|corporation|group|enterprise)?|transnational corporation|"
        r"global (?:corporation|conglomerate)|tập đoàn đa quốc gia|doanh nghiệp đa quốc gia|"
        r"tập đoàn toàn cầu)\b", re.I
    ),
    "TECH_COMPANY": re.compile(
        r"\b(?:(?:healthcare\s+)?(?:AI|technology|tech|semiconductor|chip|software|e-commerce|fintech|"
        r"biotech|cloud|cybersecurity)\s+(?:company|companies|firm|firms|maker|giant|"
        r"group|corporation|startup)|AI-focused company|tech giant|chipmaker|semiconductor maker|"
        r"technology company|technology firm|công ty công nghệ|tập đoàn công nghệ)\b", re.I
    ),
    "FINANCE_COMPANY": re.compile(
        r"\b(?:financial services company|financial institution|investment bank|fintech company|"
        r"commercial bank|central bank|retail bank|banking company|banking group|"
        r"công ty tài chính|tổ chức tài chính|ngân hàng thương mại|ngân hàng trung ương|"
        r"ngân hàng đầu tư|tập đoàn ngân hàng)\b", re.I
    ),
    "BILLIONAIRE": re.compile(r"\b(?:billionaires?|tỷ phú)\b", re.I),
}
_GENERIC_ALIASES = {
    "company", "companies", "fund", "funds", "growth", "investment", "investments",
    "venture", "ventures", "capital", "firm", "firms", "group", "bank", "banks",
    "công ty", "doanh nghiệp", "quỹ", "tập đoàn", "ngân hàng", "cổ phiếu", "usd",
    "ai", "he", "she", "they", "it", "its", "him", "her", "them", "their",
    "other billionaires", "viable startup",
    "early-stage AI startups", "startup ecosystem", "global startup ecosystem",
    "startup battlefield", "startup battlefield 200", "startup", "startups",
    "venture capital", "the startup", "các", "đây", "nhà", "điều", "việc",
    "tính", "kể", "cam kết", "âu", "his", "ceo", "khoản", "sessions",
    "breakout sessions", "disrupt", "conversation", "cybersecurity", "partnership", "bot",
    "stories", "communities", "winner", "networking", "the companies", "security", "further",
    "hàn quốc", "trung quốc", "việt nam", "united states", "china", "south korea",
    "disruptive", "tech", "school", "product", "building", "model", "team",
    "techcrunch", "techcrunch disrupt", "techcrunch startup battlefield",
    "or", "three", "number", "innovation", "technology", "chatbot", "market",
    "ecosystem", "engine", "software", "community", "vehicle", "offer", "watch",
    "teams", "breakouts", "something", "stage", "avatar", "app-building", "pitches",
    "program", "commerce", "competition", "discovery", "fintech", "aum", "mac",
    "scaling", "defense", "build", "both", "our", "this", "some", "được", "20",
    "nhật bản", "japan", "năm 2025", "next generation", "semiconductors",
    "ev", "consumer", "doanh", "nhà nước", "investors", "founders",
    "customers", "clients", "suppliers", "the company", "this company", "their company",
    "the firm", "this firm", "the fund", "the business", "the investment", "the group",
    "investor", "founder", "customer", "client", "supplier", "business", "enterprise",
    "organization", "organizations", "government", "governments", "đối tác",
    "nhà đầu tư", "nhà sáng lập", "khách hàng", "các doanh nghiệp", "cùng", "who",
    "early-stage", "ai chip", "expo hall", "machine learning", "chip", "ipo",
    "accelerators", "healthcare", "third", "known", "hardware", "products", "bitcoin",
    "series a", "khối", "sự kiện", "những", "xây dựng", "tây ban nha",
}
_GENERIC_ENTITY = re.compile(
    r"^(?:(?:the|a|an|this|that|these|those|their|our|its|his|her|một|các|những)\s+)?"
    r"(?:company|business|firm|startup|fund|investor|founder|customer|client|supplier|"
    r"enterprise|organization|bank|government|doanh nghiệp|công ty|quỹ|nhà đầu tư|"
    r"nhà sáng lập|khách hàng|đối tác|tập đoàn|ngân hàng)s?$", re.I)
_GENERIC_EDGE_WORDS = {"công", "ty", "doanh", "nghiệp", "quỹ", "tập", "đoàn", "đầu", "tư",
                       "hiện", "đang", "cùng", "và", "who", "which", "whose"}
_COUNTRY_NAMES = {
    "california",
    "canada", "russia", "nga", "japan", "nhật", "nhật bản", "india", "ấn độ",
    "china", "trung quốc", "united states", "mỹ", "hoa kỳ", "united kingdom", "anh",
    "south korea", "hàn quốc", "vietnam", "việt nam", "australia", "úc", "saudi arabia",
    "ả rập xê út", "spain", "tây ban nha", "france", "pháp", "germany", "đức", "italy",
    "ý", "brazil", "mexico", "ukraine", "ukraina", "israel", "taiwan", "đài loan",
    "indonesia", "singapore", "thailand", "thái lan", "pakistan", "turkey", "thổ nhĩ kỳ",
}
_ALLOWED_TYPES = {
    "BUSINESS_ORGANIZATION": {"ORG"},
    "STARTUP": {"ORG"}, "VC_FUND": {"ORG"}, "INVESTMENT_FUND": {"ORG"},
    "MULTINATIONAL_CORPORATION": {"ORG"}, "TECH_COMPANY": {"ORG"},
    "FINANCE_COMPANY": {"ORG"}, "BILLIONAIRE": {"PERSON"},
}
_APPOSITION_WORDS = {"a", "an", "the", "of", "named", "called", "firm", "company", "group",
                     "is", "are", "was", "were", "as", "là", "một", "nhà", "hãng", "tập", "đoàn", "công", "ty", "quỹ", "đầu",
                     "tư", "tổ", "chức", "tài", "chính", "nghệ", "quốc", "gia", "tỷ", "phú"}
_BUSINESS_NAME_SUFFIX = re.compile(
    r"\S.+\s(?:Capital|Ventures|Partners|Holdings|Bank|Technologies|Labs|Robotics|"
    r"Therapeutics|Enterprises|Materials|Corporation|Company|Group|Fund|Management|Investments|Investment Authority|Inc\.?|Ltd\.?)$")


def _mentions(text, pattern):
    return list(pattern.finditer(text))


def _distance(left, right):
    return max(0, max(left[0], right[0]) - min(left[1], right[1]))


def _nearby_words(text, mention, cue):
    gap = text[min(mention[1], cue[1]):max(mention[0], cue[0])]
    return re.findall(r"[\wÀ-ỹ]+", gap.casefold())


def _generic_alias(value):
    value = normalize(value).casefold().strip()
    words = re.findall(r"[\wÀ-ỹ]+", value)
    return (value in _GENERIC_ALIASES or bool(_GENERIC_ENTITY.fullmatch(value))
            or value in _COUNTRY_NAMES
            or bool(re.fullmatch(r"(?:19|20)\d{2}(?:[-–]\d{2,4})?", value))
            or bool(words and (words[0] in _GENERIC_EDGE_WORDS or words[-1] in _GENERIC_EDGE_WORDS)))


def _is_apposition(text, mention, cue, surface):
    gap = text[min(mention[1], cue[1]):max(mention[0], cue[0])]
    words = _nearby_words(text, mention, cue)
    short = (not any(mark in gap for mark in ".;!?\n—–") and len(words) <= 2
            and all(word in _APPOSITION_WORDS for word in words)
            and (mention[1] > cue[0] or bool(words))
            and (surface[:1].isupper() or any(char.isupper() for char in surface[1:]))
            and not (mention[0] >= cue[1] and re.match(r"^[’']s?(?:\s|$)", gap, re.I)))
    descriptive = (mention[1] <= cue[0] and len(gap) <= 140 and len(words) <= 14
                   and bool(re.match(r"^\s*,\s*(?:an?|the)\s+|^\s+(?:is|was)\s+(?:an?|the)\s+", gap, re.I))
                   and not re.search(r"[.;!?\n]|\b(?:said|says|whose|which|who|joined|backed|led|"
                                     r"raised|acquired|invested|announced|reported|claimed)\b", gap, re.I)
                   and any(char.isupper() for char in surface))
    subsidiary = (mention[1] <= cue[0] and bool(re.fullmatch(r"\s*,\s*", gap))
                  and bool(re.match(r"công ty con (?:của|thuộc)\b", text[cue[0]:], re.I)))
    return short or descriptive or subsidiary


def _write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n" for row in rows),
                    encoding="utf-8")


def _canonical_claims(rows):
    priority = {"rejected": 3, "incorrect": 3, "manually_verified": 2}
    result = {}
    for source in rows:
        row = dict(source)
        subject, object_ = row.get("subject_id"), row.get("object_id")
        if (row.get("predicate") in SYMMETRIC_RELATIONS and isinstance(subject, str)
                and isinstance(object_, str) and subject > object_):
            row["subject_id"], row["object_id"] = row["object_id"], row["subject_id"]
        identity = (row.get("subject_id"), row.get("predicate"), row.get("object_id"),
                    row.get("assertion_status"), row.get("document_id"), row.get("sentence_id"))
        if not all(value is not None for value in identity):
            result[("unkeyed", len(result))] = row
            continue
        subject, predicate, object_, status, document_id, sentence_id = identity
        event_id = stable_id(subject, predicate, object_, status, document_id)
        claim_id = stable_id(event_id, sentence_id)
        row.update(event_id=event_id, claim_id=claim_id)
        current = result.get(claim_id)
        if current is None or priority.get(row.get("review_status"), 1) > priority.get(
                current.get("review_status"), 1):
            result[claim_id] = row
    return list(result.values())


def filter_domain_export(source: Path, output: Path, *, aliases_path=Path("config/entities.yaml"),
                         targets=None) -> dict:
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
    source_entities = rows["entities"]
    canonical_entities, remap, source_names = {}, {}, defaultdict(set)
    for entity in source_entities:
        name = named_head(entity["name"]) if entity["entity_type"] == "ORG" else normalize(entity["name"])
        entity_id = (stable_id(entity["entity_type"], name.casefold())
                     if name != entity["name"] else entity["entity_id"])
        remap[entity["entity_id"]] = entity_id
        source_names[entity_id].add(entity["name"])
        canonical_entities.setdefault(entity_id, dict(entity, entity_id=entity_id, name=name))
    rows["entities"] = list(canonical_entities.values())
    rows["claims"] = [dict(row, subject_id=remap.get(row["subject_id"], row["subject_id"]),
                           object_id=remap.get(row["object_id"], row["object_id"]),
                           normalization_source_subject_id=row["subject_id"],
                           normalization_source_object_id=row["object_id"])
                      for row in rows["claims"]]
    article_by_id = {row["document_id"]: row for row in rows["articles"]}
    for claim in rows["claims"]:
        body = article_by_id.get(claim.get("document_id"), {}).get("text", "")
        text = claim.get("evidence", "")
        start = claim.get("evidence_start")
        if not isinstance(start, int) and text and body.count(text) == 1:
            start = body.index(text)
            claim.update(evidence_start=start, evidence_end=start + len(text))
        if (isinstance(start, int) and isinstance(claim.get("evidence_end"), int)
                and body[start:claim["evidence_end"]] == text):
            claim["normalization_source_sentence_id"] = claim.get("sentence_id")
            claim["sentence_id"] = stable_id(claim["document_id"], str(start), text)
    source_claim_count = len(rows["claims"])
    rows["claims"] = _canonical_claims(rows["claims"])
    rows["relations"] = _canonical_claims(rows["relations"])
    manifest = json.loads((source / "manifest.json").read_text("utf-8"))
    types = {row["entity_id"]: row["entity_type"] for row in rows["entities"]}
    entity_names = {row["entity_id"]: row["name"] for row in rows["entities"]}
    entity_by_id = {row["entity_id"]: row for row in rows["entities"]}
    recorded_mentions = {}
    mentions_file = source / "mentions.jsonl"
    if mentions_file.is_file():
        files["mentions"] = mentions_file
        recorded_mentions = {row["document_id"]: [] for row in rows["articles"]}
        for line in mentions_file.read_text("utf-8").splitlines():
            if line:
                mention = json.loads(line)
                if mention["document_id"] in recorded_mentions:
                    recorded_mentions[mention["document_id"]].append(mention)
    else:
        by_run = defaultdict(set)
        for article in rows["articles"]:
            if article.get("source_run"):
                by_run[article["source_run"]].add(article["document_id"])
        for run, document_ids in by_run.items():
            path = Path(run) / "silver/mentions.parquet"
            if path.is_file():
                recorded_mentions.update({document_id: [] for document_id in document_ids})
                for mention in pq.read_table(path).to_pylist():
                    if mention["document_id"] in document_ids:
                        recorded_mentions[mention["document_id"]].append(mention)
    aliases, curated_aliases = defaultdict(set), defaultdict(set)
    for row in yaml.safe_load(Path(aliases_path).read_text(encoding="utf-8")):
        entity_id = stable_id(row["type"], normalize(row["name"]).casefold())
        if entity_id in types:
            for name in [row["name"], *row.get("aliases", [])]:
                alias = normalize(name)
                aliases[entity_id].add(alias)
                curated_aliases[entity_id].add(alias.casefold())
    for entity in rows["entities"]:
        aliases[entity["entity_id"]].add(normalize(entity["name"]))
        aliases[entity["entity_id"]].update(source_names[entity["entity_id"]])
    name_issues = {
        entity_id: (entity_name_issue(name, types[entity_id], curated=bool(curated_aliases[entity_id]))
                    or ("generic_or_location_as_organization"
                        if types[entity_id] != "GOV" and _generic_alias(name)
                        and not curated_aliases[entity_id] else None))
        for entity_id, name in entity_names.items()
    }
    alias_ids = defaultdict(set)
    for entity_id, values in aliases.items():
        if name_issues[entity_id]:
            continue
        for value in values:
            if (len(value) >= 2 and (types[entity_id] == "GOV" or not _generic_alias(value)
                                     or value.casefold() in curated_aliases[entity_id])):
                alias_ids[value.casefold()].add(entity_id)
    alias_ids = {alias: ids for alias, ids in alias_ids.items() if len(ids) == 1}
    aliases_by_first_word = defaultdict(list)
    fallback_needed = any(article["document_id"] not in recorded_mentions for article in rows["articles"])
    for alias in alias_ids if fallback_needed else ():
        words = re.findall(r"\w+", alias.casefold())
        aliases_by_first_word[words[0] if words else ""].append(alias)
    mention_patterns = {
        first_word: re.compile(
            r"(?<!\w)(?P<name>" + "|".join(re.escape(name) for name in sorted(values, key=len, reverse=True))
            + r")(?!\w)", re.I)
        for first_word, values in aliases_by_first_word.items()
    }
    document_aliases = {}
    unresolved_contexts = defaultdict(set)
    context_entity_ids = set()
    x_org_ids = {entity_id for entity_id, name in entity_names.items() if name == "X" and types[entity_id] == "ORG"}
    for document_id, recorded in recorded_mentions.items():
        body = article_by_id[document_id].get("text", "")
        local = []
        for mention in recorded:
            entity_id = remap.get(mention["entity_id"], mention["entity_id"])
            if (types.get(entity_id) == "ORG" and not name_issues[entity_id]
                    and body[mention["start"]:mention["end"]] == mention["surface"]):
                local.append((mention["start"], mention["end"], entity_id))
        document_aliases[document_id] = organization_name_aliases(local, entity_names)
        governments = government_aliases(body)
        for mention in recorded:
            contextual = governments.get(normalize(mention["surface"]).casefold())
            if not contextual or body[mention["start"]:mention["end"]] != mention["surface"]:
                continue
            original_id = remap.get(mention["entity_id"], mention["entity_id"])
            if original_id not in types:
                continue
            canonical_id = contextual["entity_id"]
            if canonical_id not in types:
                types[canonical_id] = "GOV"
                entity_names[canonical_id] = contextual["name"]
                entity_by_id[canonical_id] = contextual
                name_issues[canonical_id] = None
                remap[canonical_id] = canonical_id
                rows["entities"].append(contextual)
                source_entities.append(dict(contextual, discovered_by="document_verified_government_alias"))
                context_entity_ids.add(canonical_id)
            document_aliases[document_id][original_id] = canonical_id
        for entity_id in x_org_ids if re.search(r"\bX\b", body) else ():
            contextual = x_organization_context(body)
            if contextual is None:
                unresolved_contexts[document_id].add(entity_id)
                continue
            canonical_id = contextual["entity_id"]
            if canonical_id not in types:
                types[canonical_id] = "ORG"
                entity_names[canonical_id] = contextual["name"]
                entity_by_id[canonical_id] = contextual
                name_issues[canonical_id] = None
                remap[canonical_id] = canonical_id
                rows["entities"].append(contextual)
                source_entities.append(dict(contextual, discovered_by="explicit_document_context"))
                context_entity_ids.add(canonical_id)
            document_aliases[document_id][entity_id] = canonical_id
    for claim in rows["claims"]:
        local = document_aliases.get(claim["document_id"], {})
        for key in ("subject_id", "object_id"):
            if claim[key] in unresolved_contexts.get(claim["document_id"], ()):
                claim["context_issue"] = "ambiguous_organization_context"
            claim[key] = local.get(claim[key], claim[key])

    def find_mentions(text, document_id=None, offset=0):
        if document_id in recorded_mentions:
            found = {}
            for mention in recorded_mentions[document_id]:
                entity_id = remap.get(mention["entity_id"], mention["entity_id"])
                if entity_id in unresolved_contexts.get(document_id, ()):
                    continue
                entity_id = document_aliases.get(document_id, {}).get(entity_id, entity_id)
                if entity_id not in types or name_issues[entity_id]:
                    continue
                start, end = mention["start"] - offset, mention["end"] - offset
                if not 0 <= start < end <= len(text) or text[start:end] != mention["surface"]:
                    continue
                surface = mention["surface"]
                name = named_head(surface) if types[entity_id] == "ORG" else surface
                start += surface.rfind(name)
                found[(start, start + len(name), entity_id)] = (start, start + len(name), entity_id, name)
            official_spans = [(start, end, entity_id) for start, end, entity_id, _ in found.values()
                              if entity_by_id[entity_id].get("resolution_method") == "document_verified_government_alias"]
            return sorted([row for row in found.values() if not (
                any(row[2] != entity_id and row[0] < end and row[1] > start
                    for start, end, entity_id in official_spans))],
                key=lambda row: (row[0], -row[1]))
        words = set(re.findall(r"\w+", text.casefold()))
        matches = [mention for first_word in words | {""} if first_word in mention_patterns
                   for mention in _mentions(text, mention_patterns[first_word])]
        matches.sort(key=lambda mention: (mention.start(), -(mention.end() - mention.start())))
        found, end = [], 0
        for mention in matches:
            if mention.start() < end:
                continue
            end = mention.end()
            entity_id = next(iter(alias_ids[normalize(mention.group("name")).casefold()]))
            surface = mention.group("name")
            name = named_head(surface) if types[entity_id] == "ORG" else surface
            start = mention.start() + surface.rfind(name)
            found.append((start, start + len(name), entity_id, name))
        return found

    tags, evidence, tagged_documents, sectors_by_document = (
        defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set))
    recovered_claims, funding_keys, derived_ids = [], set(), set()
    funding_name_index = defaultdict(list)
    for entity in entity_by_id.values():
        funding_name_index[entity["name"].casefold()].append(entity)
    for article in rows["articles"]:
        article_mentions = []
        article_sentences = list(sentences(article.get("text", "")))
        previous = None
        for sentence in article_sentences:
            text = sentence["text"]
            mentions = find_mentions(text, article["document_id"], sentence["start"])
            # A definite company reference can qualify only the sole organization in the previous sentence.
            if previous and not re.search(r"\n\s*\n", article["text"][previous["start"]:sentence["start"]]):
                referent = re.match(r"^(?:The (?:company|startup|firm)|Công ty|Doanh nghiệp)\b", text, re.I)
                prior_orgs = {entity_id for _, _, entity_id, _ in find_mentions(
                    previous["text"], article["document_id"], previous["start"])
                    if types[entity_id] == "ORG"}
                if referent and len(prior_orgs) == 1:
                    entity_id = next(iter(prior_orgs))
                    for domain_type, cue in _CUES.items():
                        if types[entity_id] not in _ALLOWED_TYPES[domain_type]:
                            continue
                        for match in cue.finditer(text):
                            if match.start() >= referent.end() and _is_apposition(
                                    text, referent.span(), match.span(), "Reference"):
                                tags[entity_id].add(domain_type)
                                evidence[entity_id].add(
                                    f"{article['document_id']}:adjacent_definite_reference:"
                                    f"{previous['text'][:240]} {text[:240]}")
                                tagged_documents[entity_id].add(article["document_id"])
            article_mentions.extend({"start": sentence["start"] + start, "end": sentence["start"] + end,
                                     "entity_id": entity_id, "entity_type": types[entity_id], "surface": surface}
                                    for start, end, entity_id, surface in mentions)
            named_mentions = [{"start": start, "end": end, "surface": surface, "entity": entity_by_id[entity_id]}
                              for start, end, entity_id, surface in mentions
                              if any(char.isupper() for char in surface) or curated_aliases[entity_id]]
            for relation in extract_relations(text, named_mentions, article.get("language", "en")):
                recovered_claims.append(dict(
                    relation, document_id=article["document_id"],
                    sentence_id=stable_id(article["document_id"], str(sentence["start"]), text),
                    evidence=text, evidence_start=sentence["start"], evidence_end=sentence["end"],
                    review_status="unreviewed", event_date="", source_run=article.get("source_run"),
                    recovery_method="explicit_sentence_construction"))
            for start, end, entity_id, surface in mentions:
                    if types[entity_id] == "GOV":
                        tags[entity_id].add("GOVERNMENT")
                        evidence[entity_id].add(f"{article['document_id']}:curated_entity_type:GOV")
                        tagged_documents[entity_id].add(article["document_id"])
                    elif types[entity_id] == "ORG":
                        if normalize(surface).casefold() in curated_aliases[entity_id]:
                            tags[entity_id].add("BUSINESS_ORGANIZATION")
                            evidence[entity_id].add(f"{article['document_id']}:curated_entity_type:ORG:{text[:240]}")
                            tagged_documents[entity_id].add(article["document_id"])
            for domain_type, cue in _CUES.items():
                for match in cue.finditer(text):
                    candidates = [(_distance((start, end), match.span()), entity_id)
                                  for start, end, entity_id, surface in mentions
                                  if types[entity_id] in _ALLOWED_TYPES[domain_type]
                                  and not (start < match.end() and match.start() < end)
                                  and _is_apposition(text, (start, end), match.span(), surface)]
                    if not candidates:
                        continue
                    distance, entity_id = min(candidates)
                    mention_span = next(((start, end) for start, end, candidate_id, _ in mentions
                                         if candidate_id == entity_id and _distance((start, end), match.span()) == distance), None)
                    if distance > 140 or mention_span is None:
                        continue
                    tags[entity_id].add(domain_type)
                    evidence[entity_id].add(
                        f"{article['document_id']}:{domain_type}:{text[:240]}")
                    tagged_documents[entity_id].add(article["document_id"])
                    if domain_type in {"TECH_COMPANY", "FINANCE_COMPANY"}:
                        sectors_by_document[(article["document_id"], entity_id)].add(domain_type)
            previous = sentence

        if article.get("language", "en") == "en":
            recovered = funding_references(article["text"], article["document_id"], article_sentences,
                                           article_mentions, entity_by_id, name_index=funding_name_index)
            for entity in recovered["entities"]:
                entity_id = entity["entity_id"]
                if entity_id in entity_by_id:
                    continue
                derived_ids.add(entity_id)
                entity_by_id[entity_id] = entity
                entity_names[entity_id], types[entity_id] = entity["name"], entity["entity_type"]
                name_issues[entity_id] = entity_name_issue(entity["name"], entity["entity_type"])
                remap[entity_id] = entity_id
                rows["entities"].append(entity)
                source_entities.append(dict(entity, discovered_by="explicit_investor_list"))
                alias_ids[entity["name"].casefold()] = {entity_id}
            for claim in recovered["claims"]:
                for key in ("subject_id", "object_id"):
                    if claim[key] in unresolved_contexts.get(article["document_id"], ()):
                        claim["context_issue"] = "ambiguous_organization_context"
                    original_id = claim[key]
                    claim[key] = document_aliases.get(article["document_id"], {}).get(original_id, original_id)
                    if claim[key] != original_id:
                        claim[f"normalization_source_{key}"] = original_id
                claim.update(source_run=article.get("source_run"), recovery_method=(
                    "explicit_investor_antecedent" if claim["rule_id"] == "en-explicit-investor-reference-v1"
                    else "explicit_round_antecedent"))
                recovered_claims.append(claim)
                funding_keys.add((claim["subject_id"], claim["object_id"], claim["document_id"],
                                  claim["evidence_start"], claim["evidence_end"]))
            if article["document_id"] in recorded_mentions:
                recorded_mentions[article["document_id"]].extend(recovered["mentions"])

    if derived_ids and fallback_needed:
        for entity_id in derived_ids:
            alias = entity_names[entity_id].casefold()
            first = re.findall(r"\w+", alias)[0]
            aliases_by_first_word[first].append(alias)
        for first in {re.findall(r"\w+", entity_names[entity_id].casefold())[0] for entity_id in derived_ids}:
            mention_patterns[first] = re.compile(
                r"(?<!\w)(?P<name>" + "|".join(re.escape(name) for name in sorted(
                    set(aliases_by_first_word[first]), key=len, reverse=True)) + r")(?!\w)", re.I)
    rows["claims"] = _canonical_claims([*rows["claims"], *recovered_claims])

    verified, claim_audit = [], []
    for claim in rows["claims"]:
        subject_id, object_id = claim.get("subject_id"), claim.get("object_id")
        constraint = RELATION_TYPES.get(claim.get("predicate"))
        article = article_by_id.get(claim.get("document_id"))
        text = claim.get("evidence", "")
        reason = None
        if claim.get("review_status") in {"rejected", "incorrect"}:
            reason = "human_rejected"
        elif claim.get("context_issue"):
            reason = claim["context_issue"]
        elif any(not claim.get(key) for key in ("claim_id", "event_id", "sentence_id", "document_id")):
            reason = "missing_claim_identity"
        elif subject_id not in types or object_id not in types:
            reason = "missing_endpoint"
        elif subject_id == object_id:
            reason = "self_edge"
        elif name_issues[subject_id] or name_issues[object_id]:
            reason = "invalid_endpoint_name"
        elif not constraint or types[subject_id] not in constraint[0] or types[object_id] not in constraint[1]:
            reason = "invalid_endpoint_types"
        elif not article or not text or text not in article.get("text", ""):
            reason = "evidence_not_in_article"
        elif (isinstance(claim.get("evidence_start"), int) and isinstance(claim.get("evidence_end"), int)
              and article["text"][claim["evidence_start"]:claim["evidence_end"]] != text):
            reason = "evidence_offset_mismatch"
        else:
            mentions = [{"start": start, "end": end, "surface": surface, "entity": entity_by_id[entity_id]}
                        for start, end, entity_id, surface in find_mentions(
                            text, claim["document_id"], claim.get("evidence_start", 0))]
            explicit_round = (claim["predicate"] == "INVESTED_IN" and
                              (subject_id, object_id, claim["document_id"], claim.get("evidence_start"),
                               claim.get("evidence_end")) in funding_keys)
            historical_ceo = claim["predicate"] == "CEO_OF" and any(
                historical_role(text, subject, object_)
                for subject in mentions if subject["entity"]["entity_id"] == subject_id
                for object_ in mentions if object_["entity"]["entity_id"] == object_id)
            if historical_ceo:
                reason = "historical_role_requires_temporal_qualification"
            elif not explicit_round and not supported_relation(
                    text, mentions, article.get("language", "en"), claim["predicate"], subject_id, object_id):
                reason = "unsupported_predicate_or_direction"
        audit = {**claim, "decision": "review" if reason else "verified", "reason": reason,
                 "subject_name": entity_names.get(subject_id), "object_name": entity_names.get(object_id),
                 "source_url": article.get("canonical_url") if article else None,
                 "article_title": article.get("title") if article else None}
        claim_audit.append(audit)
        if not reason:
            verified.append(claim)

    for claim in verified:
        if (claim["predicate"] == "INVESTED_IN" and (claim["subject_id"], claim["object_id"],
                claim["document_id"], claim.get("evidence_start"), claim.get("evidence_end")) in funding_keys):
            entity_id = claim["object_id"]
            tags[entity_id].add("FUNDED_ORGANIZATION")
            evidence[entity_id].add(f"{claim['document_id']}:explicit_funding_investors:{claim['evidence'][:240]}")
            tagged_documents[entity_id].add(claim["document_id"])
        for entity_id in (claim["subject_id"], claim["object_id"]):
            if types[entity_id] == "ORG" and _BUSINESS_NAME_SUFFIX.fullmatch(entity_names[entity_id]):
                tags[entity_id].add("BUSINESS_ORGANIZATION")
                evidence[entity_id].add(
                    f"{claim['document_id']}:business_name_and_verified_role:{claim['evidence'][:240]}")
                tagged_documents[entity_id].add(claim["document_id"])
    # One hop from evidence-qualified actors; unverified edges cannot expand the domain.
    anchors = set(tags)
    for claim in verified:
        subject_id, object_id = claim["subject_id"], claim["object_id"]
        if subject_id not in anchors and object_id not in anchors:
            continue
        for entity_id in (subject_id, object_id):
            if types[entity_id] == "ORG":
                tags[entity_id].add("BUSINESS_COUNTERPARTY")
            elif types[entity_id] == "PERSON" and claim["predicate"] in {
                    "CEO_OF", "FOUNDED", "BOARD_MEMBER_OF", "INVESTED_IN", "OWNS_STAKE_IN"}:
                tags[entity_id].add("BUSINESS_PERSON")
            else:
                continue
            evidence[entity_id].add(f"{claim['document_id']}:verified_{claim['predicate']}:{claim['evidence'][:240]}")
            tagged_documents[entity_id].add(claim["document_id"])

    for claim in verified:
        if (claim.get("predicate") == "CEO_OF"
                and types.get(claim.get("subject_id")) == "PERSON"
                and not _generic_alias(entity_names.get(claim["subject_id"], ""))
                and sectors_by_document.get((claim.get("document_id"), claim.get("object_id")))):
            tags[claim["subject_id"]].add("TECH_FINANCE_CEO")
            evidence[claim["subject_id"]].add(f"{claim['document_id']}:{claim['evidence'][:240]}")
            tagged_documents[claim["subject_id"]].add(claim["document_id"])

    for entity_id in tags:
        if types[entity_id] == "ORG" and tags[entity_id]:
            tags[entity_id].add("BUSINESS_ORGANIZATION")
    tagged = {entity_id: sorted(values) for entity_id, values in tags.items() if values}
    eligible = set(tagged)
    claims = [row for row in verified
              if row["subject_id"] in eligible and row["object_id"] in eligible]
    connected = {row[key] for row in claims for key in ("subject_id", "object_id")}
    eligible &= connected
    typed_entities = [{**entity, "domain_types": tagged[entity["entity_id"]],
                       "domain_evidence": sorted(evidence[entity["entity_id"]])[:5]}
                      for entity in rows["entities"] if entity["entity_id"] in eligible]
    article_ids = {row["document_id"] for row in claims}
    articles = [row for row in rows["articles"] if row["document_id"] in article_ids]
    triples = {}
    for row in claims:
        triples.setdefault((row["subject_id"], row["predicate"], row["object_id"]), row)

    accepted_claim_ids = {row.get("claim_id") for row in claims}
    for audit in claim_audit:
        if audit["decision"] == "verified":
            audit.update(decision="accepted" if audit.get("claim_id") in accepted_claim_ids else "review",
                         reason="verified_in_domain" if audit.get("claim_id") in accepted_claim_ids
                         else "no_domain_anchor")
    entity_audit = [{**entity, "canonical_entity_id": remap[entity["entity_id"]],
                     "canonical_name": entity_names[remap[entity["entity_id"]]],
                     "domain_types": tagged.get(remap[entity["entity_id"]], []),
                     "domain_evidence": sorted(evidence[remap[entity["entity_id"]]])[:5],
                     "decision": "accepted" if remap[entity["entity_id"]] in eligible else "review",
                     "reason": ("verified_connected_domain_entity" if remap[entity["entity_id"]] in eligible else
                                name_issues[remap[entity["entity_id"]]] or (
                                    "domain_qualified_but_unconnected" if remap[entity["entity_id"]] in tagged
                                    else "no_entity_specific_domain_evidence"))}
                    for entity in source_entities]

    counts = {"articles": len(articles), "nodes": len(typed_entities), "relations": len(triples),
              "claims": len(claims), "relation_types": len({row["predicate"] for row in claims})}
    targets = targets if targets is not None else {"nodes": 2000, "relations": 5000, "relation_types": 11}
    status = manifest.get("status", {})
    if isinstance(status, dict):
        status = {**status, "counts": counts, "reason": "domain_verified", "targets": targets,
                  "targets_met": all(counts.get(key, 0) >= value for key, value in targets.items()
                                     if value is not None),
                  "remaining": {key: max(0, value - counts.get(key, 0)) for key, value in targets.items()
                                if value is not None}}
    filtered_manifest = {**manifest, "status": status, "counts": counts,
                         "quality": {**manifest.get("quality", {}),
                                     "domain_filter": VERSION,
                                     "precision": None},
                         "domain_filter": {"version": VERSION, "types": sorted(
                             {kind for entity in typed_entities for kind in entity["domain_types"]}),
                             "excluded_entities": len(source_entities) - len(typed_entities),
                             "merged_entities": len(source_entities) - len(rows["entities"]),
                             "duplicate_claims_removed": source_claim_count + len(recovered_claims) - len(rows["claims"]),
                             "recovered_candidates": len(recovered_claims), "derived_entities": len(derived_ids),
                             "document_name_resolutions": sum(len(values) for values in document_aliases.values()),
                             "context_entities": len(context_entity_ids),
                             "unresolved_context_documents": len(unresolved_contexts),
                             "excluded_claims": len(rows["claims"]) - len(claims),
                             "entity_reasons": dict(Counter(row["reason"] for row in entity_audit)),
                             "claim_reasons": dict(Counter(row["reason"] for row in claim_audit)),
                             "audit": {"entities": "audit/entities.jsonl", "claims": "audit/claims.jsonl",
                                       "name_resolutions": "audit/name_resolutions.jsonl",
                                       "unresolved_contexts": "audit/unresolved_contexts.jsonl"}},
                         "lineage": {"source_export": str(source.resolve()),
                                     "aliases_sha256": hashlib.sha256(Path(aliases_path).read_bytes()).hexdigest(),
                                     "implementation_sha256": {
                                         name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                         for name in ("domain_filter.py", "nlp.py", "entity_quality.py", "funding.py")},
                                     "input_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest()
                                                      for name, path in files.items()}},
                         "storage_layer": "normalized"}
    output.mkdir(parents=True)
    _write_jsonl(output / "articles.jsonl", articles)
    _write_jsonl(output / "entities.jsonl", typed_entities)
    _write_jsonl(output / "relations.jsonl", list(triples.values()))
    _write_jsonl(output / "claims.jsonl", claims)
    (output / "audit").mkdir()
    _write_jsonl(output / "audit/entities.jsonl", entity_audit)
    _write_jsonl(output / "audit/claims.jsonl", claim_audit)
    _write_jsonl(output / "audit/unresolved_contexts.jsonl", [
        {"document_id": document_id, "entity_id": entity_id, "name": entity_names[entity_id],
         "reason": "ambiguous_organization_context"}
        for document_id, values in unresolved_contexts.items() for entity_id in sorted(values)])
    _write_jsonl(output / "audit/name_resolutions.jsonl", [
        {"document_id": document_id, "short_entity_id": short, "full_entity_id": full,
         "short_name": entity_names[short], "full_name": entity_names[full],
         "reason": ("document_verified_government_alias" if types[full] == "GOV"
                    else "explicit_document_context" if entity_names[short] == "X"
                    else "unique_corporate_name_expansion_in_document")}
        for document_id, values in document_aliases.items() for short, full in values.items()])
    (output / "manifest.json").write_text(
        json.dumps(filtered_manifest, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    return {"output": str(output), "counts": counts, "domain_filter": filtered_manifest["domain_filter"]}
