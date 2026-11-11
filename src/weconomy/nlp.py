"""Deterministic baseline plus optional bilingual GLiNER extraction."""
import re
import unicodedata
from pathlib import Path

import yaml
from langdetect import DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from rapidfuzz import fuzz

from .entity_quality import (
    entity_name_issue,
    government_aliases,
    historical_role,
    indirect_organization_reference,
    named_head,
    organization_person_role,
    partial_organization_name,
    possessive_person_reference,
    x_organization_context,
)
from .schema import RELATION_TYPES, SYMMETRIC_RELATIONS, stable_id

DetectorFactory.seed = 0
_PERSON_TITLES = {"ông", "bà", "anh", "chị", "cô", "bác", "ngài", "mr", "mrs", "ms", "dr", "sir", "prof"}


def document_person_aliases(entities, mentions):
    """Resolve short person references only when one full-name anchor exists in the same document."""
    full_names, surnames = {}, {}
    for entity_id, entity in entities.items():
        if entity.get("entity_type") != "PERSON":
            continue
        tokens = re.findall(r"[^\W_]+", normalize(entity["name"]).casefold())
        while tokens and tokens[0] in _PERSON_TITLES:
            tokens.pop(0)
        if len(tokens) < 2:
            continue
        full_names.setdefault(" ".join(tokens), set()).add(entity_id)
        surnames.setdefault(tokens[-1], set()).add(entity_id)

    aliases = {}
    for mention in mentions:
        entity_id = mention["entity_id"]
        entity = entities.get(entity_id, {})
        if entity.get("entity_type") != "PERSON":
            continue
        tokens = re.findall(r"[^\W_]+", normalize(mention["surface"]).casefold())
        while tokens and tokens[0] in _PERSON_TITLES:
            tokens.pop(0)
        candidates = (full_names.get(" ".join(tokens), set()) if len(tokens) > 1
                      else surnames.get(tokens[0], set()) if tokens else set())
        if len(candidates) == 1:
            canonical_id = next(iter(candidates))
            if entity_id != canonical_id:
                aliases[entity_id] = canonical_id
    return aliases


def normalize(text):
    text = unicodedata.normalize("NFC", text)
    return "\n".join(re.sub(r"[\t \u00a0]+", " ", line).strip() for line in text.splitlines()).strip()


def route(text, hint=""):
    if hint in {"vi", "en"}:
        return hint, "source_metadata"
    try:
        candidates = detect_langs(text)
    except LangDetectException:
        return "unknown", "insufficient_text"
    top = candidates[0]
    return (top.lang if top.lang in {"en", "vi"} and top.prob >= 0.8 else "unknown"), "langdetect"


def sentences(text):
    # shortcut: uncommon non-initial abbreviations still need a model segmenter.
    start = 0
    for match in re.finditer(r"[.!?]+[)\]\"”’]*(?=\s|$)|\n+|$", text):
        # Keep common abbreviations inside a continuing sentence, e.g. "the U.S. military".
        tail = text[match.end():].lstrip()
        prefix = text[:match.end()]
        if (tail and match.group() == "." and re.search(r"\b(?:[A-Z]\.){2,}$", prefix)
                and (tail[0].islower() or re.match(r"(?:Fund|Capital|Ventures|Company|Bank)\b", tail))):
            continue
        if (tail and tail[0].islower() and match.group() == "."
                and re.search(r"\b(?:U\.S|U\.K|Inc|Corp|Ltd|Co)\.$", prefix)):
            continue
        end = match.start() if match.group().startswith("\n") else match.end()
        left = start
        while left < end and text[left].isspace():
            left += 1
        if left < end:
            yield {"text": text[left:end], "start": left, "end": end}
        start = match.end()


class NLP:
    def __init__(self, config):
        self.backend = config["ner_backend"]
        if self.backend not in {"gazetteer", "models"}:
            raise ValueError("ner_backend must be gazetteer or models")
        self.model_ids = {
            "en": config.get("english_model", "knowledgator/gliner-relex-base-v1.0"),
            "vi": config.get("vietnamese_model", "belumind/barb-2-ie-vi"),
        }
        seeds = yaml.safe_load(Path(config["aliases"]).read_text(encoding="utf-8"))
        self.aliases = {}
        for row in seeds:
            for alias in [row["name"], *row["aliases"]]:
                key = normalize(alias).casefold()
                value = (row["name"], row["type"])
                if key in self.aliases and self.aliases[key] != value:
                    raise ValueError(f"Ambiguous alias: {alias}")
                self.aliases[key] = value
        self.alias_pattern = re.compile(
            r"(?<!\w)(?:" + "|".join(re.escape(x) for x in sorted(self.aliases, key=len, reverse=True))
            + r")(?!\w)", re.IGNORECASE
        )
        self.models = {"en": None, "vi": None}
        self._prediction = None
        self.validation = []
        self._span_aliases = {}
        self._document_x_context = None
        self._document_context_active = False
        self._document_governments = {}
        self._government_pattern = None

    def begin_document(self, text):
        self._document_context_active = True
        self._document_x_context = x_organization_context(text)
        self._document_governments = government_aliases(text)
        self._government_pattern = (re.compile(
            r"(?<!\w)(?:" + "|".join(re.escape(name) for name in sorted(
                self._document_governments, key=len, reverse=True)) + r")(?!\w)", re.I)
            if self._document_governments else None)

    def resolve(self, surface, entity_type):
        key = normalize(surface).casefold()
        if key in self._document_governments:
            return dict(self._document_governments[key])
        name, kind = self.aliases.get(key, (normalize(surface), entity_type))
        method = "curated_alias" if key in self.aliases else "exact_surface_type"
        if kind == "ORG" and key == "x" and self._document_context_active and self._document_x_context:
            return dict(self._document_x_context)
        return {"entity_id": stable_id(kind, name.casefold()), "name": name,
                "entity_type": kind, "resolution_method": method}

    def suggestions(self, surface, threshold=90):
        # Fuzzy matches are review suggestions; they never auto-merge entities.
        return [{"alias": alias, "score": fuzz.ratio(surface.casefold(), alias)}
                for alias in self.aliases if fuzz.ratio(surface.casefold(), alias) >= threshold]

    def audit_record(self, text, language):
        if self.backend != "models" or not self._prediction or self._prediction[:2] != (text, language):
            return None
        return {"text": text, "language": language, "entities": self._prediction[2],
                "relations": self._prediction[3], "validation": list(self.validation)}

    def mentions(self, text, language):
        self.validation = []
        self._span_aliases = {}
        if language not in {"vi", "en"}:
            return []
        spans = [(m.start(), m.end(), "", "gazetteer") for m in self.alias_pattern.finditer(text)]
        if self._government_pattern:
            spans.extend((m.start(), m.end(), "GOV", "gazetteer") for m in self._government_pattern.finditer(text))
        if self.backend == "models":
            entities, relations = self._infer(text, language)
            self._prediction = (text, language, entities, relations)
            for row in entities:
                start, end = row["start"], row["end"]
                kind = self._entity_type(row["label"], language)
                if normalize(row["text"]).casefold() in self._document_governments:
                    kind = "GOV"
                if kind and 0 <= start < end <= len(text) and text[start:end] == row["text"]:
                    name = named_head(row["text"]) if kind == "ORG" else row["text"]
                    issue = entity_name_issue(name, kind,
                                              curated=normalize(name).casefold() in self.aliases)
                    if issue:
                        self.validation.append({"kind": "entity", "reason": issue, "prediction": row})
                        continue
                    original_span = (start, end)
                    start += row["text"].rfind(name)
                    end = start + len(name)
                    self._span_aliases[original_span] = (start, end)
                    spans.append((start, end, kind, "gliner"))
                else:
                    self.validation.append({"kind": "entity", "reason": "invalid_label_or_span", "prediction": row})
        # Keep longest span at each overlap; seeds win equal spans.
        chosen = []
        for start, end, kind, method in sorted(
                spans, key=lambda x: (x[3] != "gazetteer", -(x[1] - x[0]), x[0])):
            if any(start < b and end > a for a, b, *_ in chosen):
                if method == "gliner":
                    self.validation.append({"kind": "entity", "reason": "overlapping_curated_or_longer_span",
                                            "start": start, "end": end})
                continue
            chosen.append((start, end, kind, method))
        result = []
        for start, end, kind, method in sorted(chosen):
            entity = self.resolve(text[start:end], kind or "ORG")
            if (entity["entity_type"] == "ORG" and normalize(text[start:end]).casefold() == "x"
                    and self._document_context_active and not self._document_x_context):
                self.validation.append({"kind": "entity", "reason": "ambiguous_organization_context",
                                        "start": start, "end": end, "surface": text[start:end]})
                continue
            if entity.get("resolution_method") == "explicit_document_context":
                self.validation.append({"kind": "entity_resolution", "reason": "explicit_document_context",
                                        "start": start, "end": end, "surface": text[start:end],
                                        "canonical_entity_id": entity["entity_id"], "canonical_name": entity["name"]})
            result.append({"start": start, "end": end, "surface": text[start:end], "method": method,
                           "entity": entity})
        return result

    def relations(self, text, mentions, language):
        result = extract_relations(text, mentions, language)
        if self.backend == "models" and language in self.models and relation_sentence(text, language, allow_local_roles=True):
            if not self._prediction or self._prediction[:2] != (text, language):
                entities, relations = self._infer(text, language)
            else:
                _, _, entities, relations = self._prediction
            by_span = {(m["start"], m["end"]): m for m in mentions}
            by_span.update({raw: by_span[canonical] for raw, canonical in self._span_aliases.items()
                            if canonical in by_span})
            for row in relations:
                predicate = self._predicate(row["relation"], language)
                head, tail = row["head"], row["tail"]
                subject, object_ = by_span.get((head["start"], head["end"])), by_span.get(
                    (tail["start"], tail["end"]))
                if not predicate or not subject or not object_:
                    self.validation.append({"kind": "relation", "reason": "missing_valid_endpoint",
                                            "prediction": row})
                    continue
                if subject["entity"]["entity_id"] == object_["entity"]["entity_id"]:
                    self.validation.append({"kind": "relation", "reason": "self_edge", "prediction": row})
                    continue
                constraints = RELATION_TYPES.get(predicate)
                if constraints and (subject["entity"]["entity_type"] not in constraints[0]
                                    or object_["entity"]["entity_type"] not in constraints[1]):
                    self.validation.append({"kind": "relation", "reason": "invalid_endpoint_types", "prediction": row})
                    continue
                if predicate == "CEO_OF" and historical_role(text, subject, object_):
                    self.validation.append({"kind": "relation", "reason": "historical_role_requires_temporal_qualification",
                                            "prediction": row})
                    continue
                if not supported_relation(text, mentions, language, predicate,
                                          subject["entity"]["entity_id"], object_["entity"]["entity_id"]):
                    self.validation.append({"kind": "relation", "reason": "unsupported_predicate_or_direction",
                                            "prediction": row})
                    continue
                left_end = min(head["end"], tail["end"])
                right_start = max(head["start"], tail["start"])
                trigger = text[left_end:right_start].strip() or row["relation"]
                result.append({"subject_id": subject["entity"]["entity_id"], "predicate": predicate,
                               "object_id": object_["entity"]["entity_id"], "trigger": trigger,
                               "rule_id": f"gliner-{language}-relex-v1", "assertion_status": "reported"})
        unique = {}
        for claim in result:
            unique.setdefault((claim["subject_id"], claim["predicate"], claim["object_id"]), claim)
        return list(unique.values())

    def _infer(self, text, language):
        if self.models[language] is None:
            from gliner import GLiNER
            self.models[language] = GLiNER.from_pretrained(self.model_ids[language])
        entities, relations = self.models[language].inference(
            texts=[text], labels=ENTITY_LABELS[language], relations=relation_label_candidates(text, language),
            threshold=0.5 if language == "vi" else 0.4,
            relation_threshold=0.6 if language == "vi" else 0.7,
            return_relations=True, flat_ner=False,
        )
        return entities[0], relations[0]

    @staticmethod
    def _entity_type(label, language):
        return ENTITY_TYPES[language].get(normalize(label).casefold())

    @staticmethod
    def _predicate(label, language):
        return RELATION_LABELS[language].get(normalize(label).casefold())



# Exact between-mention patterns avoid sentence-wide co-occurrence edges.
RULES = {
    "en": {
        "ACQUIRED": r"(?:has |had )?(?:acquired|bought|purchased|buys|acquires)",
        "AGREED_TO_ACQUIRE": r"(?:has |had )?agreed to (?:acquire|buy)",
        "INVESTED_IN": r"(?:has )?invested in",
        "MERGED_WITH": r"(?:has )?merged with",
        "SUED": r"(?:has )?(?:sued|sues)",
        "PARTNERED_WITH": r"(?:has )?partnered with",
        "SUPPLIES_TO": r"(?:supplies|supplied)(?: components| chips| equipment)? to",
        "CEO_OF": r"(?:is|was)(?: the)? (?:CEO|chief executive officer) of",
        "FOUNDED": r"(?:co-)?founded",
        "SUBSIDIARY_OF": r"(?:is|was) a subsidiary of",
        "REGULATES": r"(?:regulates|regulated)",
        "OWNS_STAKE_IN": r"(?:owns|holds)(?: a)?(?: minority| majority)?(?: equity)? stake in|holds shares in",
        "BOARD_MEMBER_OF": r"(?:is|was)(?: a)? board member of|serves on the board of",
        "CONTRACTED_WITH": r"(?:signed|entered into) a contract with",
        "AWARDED_CONTRACT_TO": r"awarded (?:a )?(?:contract|deal) to",
        "ANTITRUST_ACTION_AGAINST": r"(?:filed|brought) (?:an? )?antitrust (?:action|case|proceedings) against",
        "SANCTIONED": r"(?:imposed sanctions on|sanctioned)",
        "DISRUPTED_SUPPLY_TO": r"(?:disrupted|halted) (?:the )?supply to",
        "SPUN_OFF_FROM": r"spun off from",
        "INVESTIGATES": r"(?:is |was |has been )?(?:also )?(?:investigating|probing)(?: whether)?(?: (?:[\w-]+ ){0,3}(?:company|startup|firm))?",
        "CLOSED_INVESTIGATION_INTO": r"(?:has |had )?(?:closed|ended|dropped|dismissed) (?:its|the|an?) (?:[\w-]+ ){0,3}(?:investigation|probe) (?:into|of|against)(?: (?:[\w-]+ ){0,3}(?:company|startup|firm))?",
        "LICENSED_TECH_FROM": r"(?:has )?licensed (?:technology|tech|intellectual property|IP) from",
    },
    "vi": {
        "ACQUIRED": r"(?:đã )?(?:mua lại|thâu tóm)",
        "AGREED_TO_ACQUIRE": r"(?:đã )?(?:đạt thỏa thuận|thỏa thuận) (?:mua lại|thâu tóm)",
        "INVESTED_IN": r"(?:đã )?đầu tư vào",
        "MERGED_WITH": r"(?:đã )?sáp nhập với",
        "SUED": r"(?:đã )?kiện",
        "PARTNERED_WITH": r"(?:đã )?(?:ký kết )?(?:thỏa thuận )?hợp tác với",
        "SUPPLIES_TO": r"cung cấp (?:linh kiện |chip )?cho",
        "CEO_OF": r"là (?:CEO|tổng giám đốc|giám đốc điều hành) của",
        "FOUNDED": r"(?:đã )?(?:đồng )?thành lập",
        "SUBSIDIARY_OF": r"là công ty con của",
        "REGULATES": r"quản lý hoạt động của",
        "OWNS_STAKE_IN": r"(?:sở hữu|nắm giữ)(?: một phần)? (?:cổ phần|cổ phiếu) tại",
        "BOARD_MEMBER_OF": r"(?:là )?thành viên (?:hội đồng quản trị|HĐQT) của",
        "CONTRACTED_WITH": r"(?:đã )?(?:ký|kí) hợp đồng với",
        "AWARDED_CONTRACT_TO": r"(?:đã )?(?:trao|giao) hợp đồng cho",
        "ANTITRUST_ACTION_AGAINST": r"(?:đã )?(?:khởi kiện|đệ đơn kiện) chống độc quyền (?:đối với|nhằm vào)",
        "SANCTIONED": r"(?:đã )?(?:áp đặt lệnh trừng phạt|áp đặt trừng phạt) (?:lên|đối với)",
        "DISRUPTED_SUPPLY_TO": r"(?:đã )?(?:làm gián đoạn|làm đình trệ) nguồn cung (?:cho|tới|đến)",
        "SPUN_OFF_FROM": r"(?:đã )?(?:tách ra|tách mình) khỏi",
        "INVESTIGATES": r"(?:đang |đã )?điều tra",
        "CLOSED_INVESTIGATION_INTO": r"(?:đã )?(?:kết thúc|đóng|chấm dứt) (?:cuộc |việc )?điều tra (?:đối với|về)",
        "LICENSED_TECH_FROM": r"(?:đã )?(?:mua|nhận) (?:quyền sử dụng|giấy phép sử dụng) công nghệ từ",
    },
}
NEGATIVE = re.compile(
    r"\b(?:not|never|no|denied|denies|if|whether|rumou?r(?:ed)?|reportedly|allegedly|"
    r"không|chưa|phủ nhận|nếu|tin đồn)\b", re.I
)
VI_UNCERTAIN = re.compile(r"(?:^\s*liệu\b|\b(?:chưa rõ|không biết|cân nhắc|xem xét)\s+liệu\b)", re.I)
GOVERNMENT_ACTIONS = {"INVESTIGATES", "CLOSED_INVESTIGATION_INTO"}

# These patterns have the opposite surface order from the graph edge.
REVERSE_RULES = {
    "en": {
        "ACQUIRED": (r"(?:was|has been|had been) (?:acquired|bought|purchased)(?: in \d{4})? by"
                     r"(?: (?:another|an?|the) (?:[\w-]+ ){0,3}(?:company|startup|firm),)?"),
        "SUED": r"(?:was|has been) sued by",
        "FOUNDED": r"(?:was|has been) (?:co-)?founded by",
        "INVESTIGATES": r"(?:is|was|has been) (?:still )?under investigation by(?: the)?",
    },
    "vi": {
        "ACQUIRED": r"(?:đã )?được mua lại bởi",
        "SUED": r"(?:đã )?bị kiện bởi",
        "FOUNDED": r"(?:đã )?được (?:đồng )?thành lập bởi",
    },
}

ROLE_RULES = {
    "en": [
        ("CEO_OF", r",\s*(?:the )?(?:(?:co-)?founder and )?(?:CEO|chief executive officer) of", False),
        ("FOUNDED", r",\s*(?:the )?(?:co-)?founder(?: and (?:CEO|chief executive officer))? of", False),
        ("CEO_OF", r"(?:[’']s\s+)?(?:(?:co-)?founder and )?(?:CEO|chief executive officer)", True),
        ("FOUNDED", r"(?:[’']s\s+)?(?:co-)?founder(?: and (?:CEO|chief executive officer))?", True),
        ("FOUNDED", r",\s*(?:a|an|the)\s+(?:[\w-]+\s+){0,5}(?:startup|company|firm)\s+(?:co-)?founded by", True),
    ],
    "vi": [
        ("CEO_OF", r"(?:,\s*|[-—–]\s*)(?:là\s+)?(?:CEO|giám đốc điều hành|tổng giám đốc(?:\s+điều hành)?)(?:\s+(?:của|tại))?", False),
        ("CEO_OF", r"(?:,\s*|[-—–]\s*)?(?:là\s+)?(?:CEO|giám đốc điều hành|tổng giám đốc(?:\s+điều hành)?)(?:\s+(?:của|tại))?", True),
        ("FOUNDED", r"(?:,\s*|[-—–]\s*)?(?:là\s+)?(?:nhà\s+)?(?:đồng\s+)?sáng lập(?:\s+và\s+(?:CEO|giám đốc điều hành|tổng giám đốc(?:\s+điều hành)?))?(?:\s+của)?", False),
        ("FOUNDED", r"(?:,\s*|[-—–]\s*)?(?:là\s+)?(?:nhà\s+)?(?:đồng\s+)?sáng lập(?:\s+và\s+(?:CEO|giám đốc điều hành|tổng giám đốc(?:\s+điều hành)?))?(?:\s+của)?", True),
        ("CEO_OF", r"(?:,\s*|[-—–]\s*)?(?:là\s+)?(?:nhà\s+)?(?:đồng\s+)?sáng lập\s+và\s+(?:CEO|giám đốc điều hành|tổng giám đốc(?:\s+điều hành)?)(?:\s+của)?", False),
        ("CEO_OF", r"(?:,\s*|[-—–]\s*)?(?:là\s+)?(?:nhà\s+)?(?:đồng\s+)?sáng lập\s+và\s+(?:CEO|giám đốc điều hành|tổng giám đốc(?:\s+điều hành)?)(?:\s+của)?", True),
        ("SUBSIDIARY_OF", r"(?:,\s*|[-—–]\s*|\(\s*)(?:là\s+)?(?:một\s+)?công ty con\s+(?:của|thuộc)", False),
    ],
}


def outside_quotes(text, start, end):
    """Allow a named role outside quotations, including a closing curly quote at segment start."""
    quotes = [(i, c) for i, c in enumerate(text) if c in '\u201c\u201d"']
    inside = bool(quotes and quotes[0][1] == '\u201d')
    for i, char in enumerate(text[:end]):
        if char == '\u201c':
            inside = True
        elif char == '\u201d':
            inside = False
        elif char == '"':
            inside = not inside
        if i >= start and (inside or char in '\u201c\u201d"'):
            return False
    return True


def relation_sentence(text, language, *, allow_quotes=False, allow_local_roles=False):
    # Exclude headline fragments: a headline can compress a proposed deal into a completed-looking verb.
    if (not text.rstrip(')]"”’').endswith((".", "!")) or language not in RULES
            or (NEGATIVE.search(text) and not allow_local_roles)
            or (language == "vi" and VI_UNCERTAIN.search(text))):
        return False
    # shortcut: quoted statements and hypothetical tense abstain until attribution parsing exists.
    if '?' in text or (not allow_quotes and any(char in text for char in ['"', '“', '”'])):
        return False
    return True


def role_scope_asserted(text, left, right):
    if NEGATIVE.search(text[left["start"]:right["end"]]):
        return False
    prefix = re.split(r'[.!?;\n"“”]|\b(?:but|however|nhưng)\b',
                      text[max(0, left["start"] - 100):left["start"]], flags=re.I)[-1]
    forecast_role = re.search(
        r"\b(?:potential|future|prospective|expected(?: to be)?|would be|could be|might be|"
        r"plans? to (?:appoint|become))\s+(?:the\s+)?$", prefix, re.I)
    return not NEGATIVE.search(prefix) and not forecast_role


def extract_relations(text, mentions, language):
    if not relation_sentence(text, language, allow_quotes=True, allow_local_roles=True):
        return []
    strict = relation_sentence(text, language)
    result = []
    for left, right in zip(mentions, mentions[1:]):
        if any(row["entity"]["entity_type"] == "ORG" and partial_organization_name(text, row["end"])
               for row in (left, right)):
            continue
        gap = text[left["end"]:right["start"]].strip()
        # Buying "GitHub's assets" is not acquiring GitHub; coordinated objects need full parsing.
        coordinated = bool(re.match(r"(?:[’']s\b|\s+(?:and|or|và|hoặc)\b)",
                                    text[right["end"]:], flags=re.I))
        if re.match(r"[’']s\b", text[right["end"]:], flags=re.I):
            continue
        if len(gap) > 120 or left["entity"]["entity_id"] == right["entity"]["entity_id"]:
            continue
        rules = ([(p, pattern, False, False) for p, pattern in RULES[language].items() if p not in GOVERNMENT_ACTIONS]
                 + [(p, pattern, True, False) for p, pattern in REVERSE_RULES[language].items() if p not in GOVERNMENT_ACTIONS]
                 if not coordinated else []) if strict else []
        if outside_quotes(text, left["start"], right["end"]):
            if role_scope_asserted(text, left, {"end": left["end"]}):
                rules += [(p, RULES[language][p], False, True) for p in GOVERNMENT_ACTIONS]
                rules += [(p, pattern, True, True) for p, pattern in REVERSE_RULES[language].items()
                          if p in GOVERNMENT_ACTIONS]
            if role_scope_asserted(text, left, right):
                rules += [(*rule, True) for rule in ROLE_RULES[language]]
                if not strict:
                    rules += [(p, pattern, False, True) for p, pattern in RULES[language].items()
                              if p in {"CEO_OF", "FOUNDED", "BOARD_MEMBER_OF"}]
        for predicate, pattern, reverse, role_rule in rules:
            if not role_rule and predicate != "AGREED_TO_ACQUIRE" and _UNCOMPLETED.search(text):
                continue
            if not re.fullmatch(pattern, gap, flags=re.I):
                continue
            subject, object_ = (right, left) if reverse else (left, right)
            if subject["entity"]["entity_type"] == "PERSON" and possessive_person_reference(text, subject["end"]):
                continue
            if predicate == "CEO_OF" and historical_role(text, subject, object_):
                continue
            if (predicate == "FOUNDED" and subject["entity"]["entity_type"] == "ORG"
                    and organization_person_role(text, subject["end"])):
                continue
            if ((subject["entity"]["entity_type"] == "ORG" and indirect_organization_reference(text, subject["start"]))
                    or (predicate != "SUBSIDIARY_OF" and object_["entity"]["entity_type"] == "ORG"
                        and indirect_organization_reference(text, object_["start"]))):
                continue
            constraints = RELATION_TYPES.get(predicate)
            if (constraints and (subject["entity"]["entity_type"] not in constraints[0]
                    or object_["entity"]["entity_type"] not in constraints[1])
                    or (role_rule and predicate == "FOUNDED"
                        and subject["entity"]["entity_type"] != "PERSON")):
                continue
            result.append({"subject_id": subject["entity"]["entity_id"], "predicate": predicate,
                           "object_id": object_["entity"]["entity_id"], "trigger": gap,
                           "rule_id": f"{language}-{predicate}-{'reverse' if reverse else 'direct'}-v2",
                           "assertion_status": ("agreement_reported" if predicate == "AGREED_TO_ACQUIRE"
                                                else "historical_reported" if predicate == "INVESTIGATES"
                                                and re.search(r"\b(?:was|had|investigated)\b", gap, re.I) else "reported")})
    if language == "en" and strict and not _UNCOMPLETED.search(text):
        result.extend(funding_round_relations(text, mentions))
        result.extend(appositive_relations(text, mentions))
        result.extend(license_payment_relations(text, mentions))
    return result


def license_payment_relations(text, mentions):
    result = []
    for left, right in zip(mentions, mentions[1:]):
        if (left["entity"]["entity_type"] != "ORG" or right["entity"]["entity_type"] != "ORG"
                or left["entity"]["entity_id"] == right["entity"]["entity_id"]
                or indirect_organization_reference(text, left["start"])
                or not re.fullmatch(r"\s+paid\s+", text[left["end"]:right["start"]], re.I)
                or not re.match(r"\s+(?:US\$|[$£€])\d[\d,.]*\s+(?:million|billion)\s+to license "
                                r"(?:its|their) (?:technology|tech|intellectual property|IP)\b", text[right["end"]:], re.I)):
            continue
        result.append({"subject_id": left["entity"]["entity_id"], "predicate": "LICENSED_TECH_FROM",
                       "object_id": right["entity"]["entity_id"], "trigger": text[left["end"]:right["end"]],
                       "rule_id": "en-LICENSED_TECH_FROM-paid-v1", "assertion_status": "reported"})
    return result


def appositive_relations(text, mentions):
    """Bind a named company across a bounded descriptive clause, without rewriting evidence."""
    if not re.search(r"\b(?:announced|said)\b.{0,65}\b(?:acquired|bought|purchased)\b", text):
        return []
    result = []
    organizations = [row for row in mentions if row["entity"]["entity_type"] == "ORG"]
    for left in organizations:
        for right in organizations:
            if (not 0 < right["start"] - left["end"] <= 300
                    or left["entity"]["entity_id"] == right["entity"]["entity_id"]
                    or indirect_organization_reference(text, left["start"])):
                continue
            gap = text[left["end"]:right["start"]]
            pattern = (r",\s*(?:a|an|the)\s+[^,;!?]{1,140},\s*(?:announced|said)"
                       r"(?: on (?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))?"
                       r" that it (?:has |had )?(?:acquired|bought|purchased) (?:the |a |an )?"
                       r"(?:[\w-]+\s+){0,5}(?:startup|company|firm)\s+")
            if (not re.fullmatch(pattern, gap, re.I) or re.search(r"\b(?:stake|shares|assets|division)\b", gap, re.I)
                    or partial_organization_name(text, right["end"]) or organization_person_role(text, right["end"])):
                continue
            result.append({"subject_id": left["entity"]["entity_id"], "predicate": "ACQUIRED",
                           "object_id": right["entity"]["entity_id"], "trigger": gap,
                           "rule_id": "en-ACQUIRED-appositive-v1", "assertion_status": "reported"})
    return result


_MODEL_SUPPORT = {
    "en": {
        "INVESTED_IN": (r"\b(?:invested in|investment in|backed|led (?:the |a )?(?:\w+ ){0,3}(?:round|investment) (?:in|for))\b",
                        r"\b(?:backed by|(?:funding|investment|financing) from|led by)\b"),
        "PARTNERED_WITH": (r"\b(?:partnered with|partnership with|partnership agreement with)\b", ""),
        "ACQUIRED": (r"\b(?:acquired|bought|purchased)\b", r"\b(?:acquired|bought|purchased) by\b"),
        "AGREED_TO_ACQUIRE": (r"\b(?:agreed|agreement) to (?:acquire|buy|purchase)\b", ""),
        "MERGED_WITH": (r"\b(?:merged with|merger with)\b", ""),
        "SUED": (r"\b(?:sued|filed (?:a )?lawsuit against)\b", r"\bsued by\b"),
        "SUPPLIES_TO": (r"\b(?:supplies|supplied|provides|provided)\b.{0,70}\b(?:to|for)\b", ""),
        "SUBSIDIARY_OF": (r"\bsubsidiary of\b", ""),
        "OWNS_STAKE_IN": (r"\b(?:owns|holds|acquired|bought)\b.{0,50}\b(?:stake|shares) in\b", ""),
        "BOARD_MEMBER_OF": (r"\b(?:board member of|on the board of|joined the board of)\b", ""),
        "CONTRACTED_WITH": (r"\b(?:signed|entered into)\b.{0,40}\bcontract with\b", ""),
        "AWARDED_CONTRACT_TO": (r"\bawarded\b.{0,50}\bcontract to\b", ""),
        "ANTITRUST_ACTION_AGAINST": (r"\b(?:filed|brought) (?:an? )?antitrust (?:action|case|proceedings) against\b", ""),
        "SPUN_OFF_FROM": (r"\bspun (?:off|out) (?:of|from)\b", ""),
    },
    "vi": {
        "INVESTED_IN": (r"\b(?:đầu tư|rót vốn) vào\b", r"\b(?:nhận|huy động)\b.{0,55}\b(?:vốn|đầu tư) từ\b"),
        "PARTNERED_WITH": (r"\bhợp tác với\b", ""),
        "ACQUIRED": (r"\b(?:mua lại|thâu tóm)\b", r"\bđược (?:mua lại|thâu tóm) bởi\b"),
        "SUED": (r"\b(?:kiện|đệ đơn kiện)\b", r"\bbị kiện bởi\b"),
        "SUBSIDIARY_OF": (r"\bcông ty con (?:của|thuộc)\b", ""),
        "OWNS_STAKE_IN": (r"\b(?:sở hữu|nắm giữ|mua)\b.{0,45}\b(?:cổ phần|cổ phiếu) (?:tại|của)\b", ""),
        "BOARD_MEMBER_OF": (r"\bthành viên (?:hội đồng quản trị|HĐQT) (?:của|tại)\b", ""),
    },
}
_UNCOMPLETED = re.compile(
    r"\b(?:would|could|might|may|plans? to|planning to|wants? to|aims? to|considering|"
    r"considered|in talks|potential|expected to|dự kiến|dự định|có thể|muốn|sẽ|cân nhắc|"
    r"xem xét|thảo luận|đàm phán|kế hoạch|dự tính|có ý định|tiềm năng)\b", re.I)


def supported_relation(text, mentions, language, predicate, subject_id, object_id):
    """Corroborate a model candidate with named endpoints and a directional lexical construction."""
    if predicate not in {"CEO_OF", "FOUNDED", "BOARD_MEMBER_OF", "AGREED_TO_ACQUIRE", *GOVERNMENT_ACTIONS} and _UNCOMPLETED.search(text):
        return False
    if predicate == "OWNS_STAKE_IN" and re.search(r"\b(?:agreed|agreement|đồng ý|thỏa thuận|proposed)\b", text, re.I):
        return False
    symmetric = predicate in SYMMETRIC_RELATIONS
    for row in extract_relations(text, mentions, language):
        if row["predicate"] == predicate and (
                (row["subject_id"], row["object_id"]) == (subject_id, object_id)
                or symmetric and (row["object_id"], row["subject_id"]) == (subject_id, object_id)):
            return True
    if not relation_sentence(text, language) or _UNCOMPLETED.search(text):
        return False
    patterns = _MODEL_SUPPORT.get(language, {}).get(predicate, (RULES.get(language, {}).get(predicate, ""), ""))
    ordered = sorted(mentions, key=lambda row: row["start"])
    for left, right in zip(ordered, ordered[1:]):
        if any(row["entity"]["entity_type"] == "ORG" and partial_organization_name(text, row["end"])
               for row in (left, right)):
            continue
        ids = (left["entity"]["entity_id"], right["entity"]["entity_id"])
        if ids not in {(subject_id, object_id), (object_id, subject_id)}:
            continue
        subject, object_ = (left, right) if ids == (subject_id, object_id) else (right, left)
        if subject["entity"]["entity_type"] == "PERSON" and possessive_person_reference(text, subject["end"]):
            continue
        if predicate == "CEO_OF" and historical_role(text, subject, object_):
            continue
        if (predicate == "FOUNDED" and subject["entity"]["entity_type"] == "ORG"
                and organization_person_role(text, subject["end"])):
            continue
        if ((subject["entity"]["entity_type"] == "ORG" and indirect_organization_reference(text, subject["start"]))
                or (predicate != "SUBSIDIARY_OF" and object_["entity"]["entity_type"] == "ORG"
                    and indirect_organization_reference(text, object_["start"]))):
            continue
        gap = text[left["end"]:right["start"]].strip()
        if (ids == (object_id, subject_id) and language == "en"
                and re.fullmatch(r",?\s*which", gap, re.I)
                and predicate in {"ACQUIRED", "FOUNDED", "SUED"}):
            verb = {"ACQUIRED": "acquired|bought|purchased", "FOUNDED": "(?:co-)?founded", "SUED": "sued"}[predicate]
            tail = text[right["end"]:]
            if re.match(r"\s+(?:(?:has|had)\s+)?(?:" + verb + r")\b", tail, re.I) and not re.match(
                    r"\s+(?:acquired|bought|purchased)\s+(?:a |the )?(?:stake|shares|assets)\b", tail, re.I):
                return True
        if (len(gap) > 180 or re.match(r"[’']s\b", gap, re.I)
                or re.search(r"[;!?]|\b(?:while|whereas|although|nhưng|trong khi)\b", gap, re.I)
                or re.match(r"[’']s\b", text[right["end"]:], re.I)):
            continue
        direct = ids == (subject_id, object_id) or symmetric
        pattern = patterns[0 if direct else 1]
        match = re.search(pattern, gap, re.I) if pattern else None
        if not match:
            continue
        if predicate == "SUPPLIES_TO" and (re.search(
                r"\b(?:that|which|who|whose|can|could|may|would|will|developers|users|customers|they)\b",
                match.group(), re.I) or re.search(r"\b(?:like|such as|including|tools)\b", gap[match.end():], re.I)):
            continue
        if re.search(r"\b(?:of|by|của|bởi|tỷ phú|CEO|founder)\b", gap[match.end():], re.I):
            continue
        if direct and predicate in {"ACQUIRED", "SUED"} and re.search(r"\bby\b|\bbởi\b|\bbị\b|\bđược\b", gap, re.I):
            continue
        if predicate == "ACQUIRED" and re.search(
                r"\b(?:stake|shares|assets|business unit|division|cổ phần|cổ phiếu|tài sản)\b", gap, re.I):
            continue
        if predicate == "ACQUIRED" and re.search(r"\b(?:agreed|agreement|thỏa thuận)\b", gap, re.I):
            continue
        if predicate == "INVESTED_IN" and re.search(r"\bled by\b", gap, re.I) and not re.search(
                r"\b(?:raised|funding|financing|round|investment)\b", text, re.I):
            continue
        return True
    return False


def relation_label_candidates(text, language):
    """Avoid asking the model for predicates that lack an explicit lexical cue."""
    if not relation_sentence(text, language, allow_quotes=True, allow_local_roles=True):
        return []
    predicates = set()
    patterns = [(predicate, pattern) for rules in (RULES, REVERSE_RULES)
                for predicate, pattern in rules.get(language, {}).items()]
    patterns += [(predicate, pattern) for predicate, pattern, _ in ROLE_RULES.get(language, [])]
    patterns += [(predicate, pattern) for predicate, pair in _MODEL_SUPPORT.get(language, {}).items()
                 for pattern in pair if pattern]
    for predicate, pattern in patterns:
        if re.search(pattern, text, re.I):
            predicates.add(predicate)
    if language == "en" and re.search(r"\bpaid\b.{0,80}\bto license (?:its|their) technology\b", text):
        predicates.add("LICENSED_TECH_FROM")
    if _UNCOMPLETED.search(text):
        predicates &= {"CEO_OF", "FOUNDED", "BOARD_MEMBER_OF", "AGREED_TO_ACQUIRE", *GOVERNMENT_ACTIONS}
    if NEGATIVE.search(text):
        predicates &= {"CEO_OF", "FOUNDED", "BOARD_MEMBER_OF", *GOVERNMENT_ACTIONS}
    return [label for label, predicate in RELATION_LABELS[language].items() if predicate in predicates]


ENTITY_LABELS = {
    "en": {"person": "A named individual person, excluding pronouns and job titles",
           "organization": ("A named company, bank, investment fund or organization; exclude financing "
                            "rounds, products, events and unnamed groups"),
           "place": "A named geographic place",
           "government": "A named government, ministry, court or regulatory agency, excluding private companies"},
    "vi": ["người", "tổ chức", "địa điểm", "chính phủ hoặc cơ quan quản lý nhà nước được định danh"],
}
ENTITY_TYPES = {
    "en": {"person": "PERSON", "organization": "ORG", "place": "PLACE", "government": "GOV"},
    "vi": {"người": "PERSON", "tổ chức": "ORG", "địa điểm": "PLACE",
           "chính phủ hoặc cơ quan quản lý nhà nước được định danh": "GOV"},
}
RELATION_LABELS = {
    "en": {
        "acquired": "ACQUIRED", "agreed to acquire": "AGREED_TO_ACQUIRE", "invested in": "INVESTED_IN",
        "merged with": "MERGED_WITH", "sued": "SUED", "partnered with": "PARTNERED_WITH",
        "supplies to": "SUPPLIES_TO", "is ceo of": "CEO_OF", "founded": "FOUNDED",
        "is subsidiary of": "SUBSIDIARY_OF", "regulates": "REGULATES",
        "owns a stake in": "OWNS_STAKE_IN", "holds shares in": "OWNS_STAKE_IN",
        "board member of": "BOARD_MEMBER_OF", "serves on the board of": "BOARD_MEMBER_OF",
        "signed a contract with": "CONTRACTED_WITH", "awarded a contract to": "AWARDED_CONTRACT_TO",
        "antitrust action against": "ANTITRUST_ACTION_AGAINST", "sanctioned": "SANCTIONED",
        "disrupted supply to": "DISRUPTED_SUPPLY_TO", "spun off from": "SPUN_OFF_FROM",
        "investigates": "INVESTIGATES", "closed investigation into": "CLOSED_INVESTIGATION_INTO",
        "licensed technology from": "LICENSED_TECH_FROM",
    },
    "vi": {
        "mua lại": "ACQUIRED", "đạt thỏa thuận mua lại": "AGREED_TO_ACQUIRE", "đầu tư vào": "INVESTED_IN",
        "sáp nhập với": "MERGED_WITH", "kiện": "SUED", "hợp tác với": "PARTNERED_WITH",
        "cung cấp cho": "SUPPLIES_TO", "là tổng giám đốc của": "CEO_OF", "thành lập": "FOUNDED",
        "là công ty con của": "SUBSIDIARY_OF", "quản lý hoạt động của": "REGULATES",
        "nắm giữ cổ phần tại": "OWNS_STAKE_IN", "sở hữu cổ phần tại": "OWNS_STAKE_IN",
        "thành viên hội đồng quản trị của": "BOARD_MEMBER_OF", "thành viên hđqt của": "BOARD_MEMBER_OF",
        "ký hợp đồng với": "CONTRACTED_WITH", "trao hợp đồng cho": "AWARDED_CONTRACT_TO",
        "khởi kiện chống độc quyền nhằm vào": "ANTITRUST_ACTION_AGAINST",
        "áp đặt trừng phạt đối với": "SANCTIONED", "làm gián đoạn nguồn cung cho": "DISRUPTED_SUPPLY_TO",
        "tách ra khỏi": "SPUN_OFF_FROM",
        "điều tra": "INVESTIGATES", "kết thúc điều tra đối với": "CLOSED_INVESTIGATION_INTO",
        "nhận quyền sử dụng công nghệ từ": "LICENSED_TECH_FROM",
    },
}


_FUNDING_RAISE = re.compile(r"\b(?:raised|secured|closed)\b", re.I)
_FUNDING_CONTEXT = re.compile(
    r"\s+(?:an?\s+)?(?:(?:US\$|[$£€])?\d[\d,.]*(?:\s+(?:million|billion|m|bn))?\s+)?(?:in\s+)?(?:an?\s+)?"
    r"(?:pre-seed|seed|series\s+[a-f]|equity(?:\s+financing)?)(?:\s+funding)?\s+round\s*", re.I,
)
_FUNDING_TRIGGER = re.compile(r"\b(?:(?:co-)?led by|with participation from)\b", re.I)
_FUNDING_DEBT = re.compile(r"\b(?:loan|debt|credit facility|convertible|acquisition financing)\b", re.I)
_FUNDING_SUBJECT_GAP = re.compile(r"\s*(?:(?:has|recently|just|successfully|also)\s+){0,2}", re.I)
_FUNDING_LIST_GAP = re.compile(r"(?:\s*,\s*(?:and\s+)?|\s+and(?:\s+co-led by)?\s+|\s*&\s*)", re.I)


def funding_round_relations(text, mentions):
    """Connect named endpoints only around explicit completed equity-stage lead clauses."""
    result = []
    emitted = set()
    for trigger in _FUNDING_TRIGGER.finditer(text):
        delimiters = [m.start() for m in re.finditer(r"[;?!\n]|(?<!\d)\.(?!\d)", text)]
        before = [pos for pos in delimiters if pos < trigger.start()]
        after = [pos for pos in delimiters if pos >= trigger.end()]
        sentence_start = before[-1] + 1 if before else 0
        sentence_end = after[0] if after else len(text)
        raises = list(_FUNDING_RAISE.finditer(text, sentence_start, trigger.start()))
        if not raises:
            continue
        raise_verb = raises[-1]
        context = re.split(r"\b(?:co-)?led by\b|\bwith participation from\b",
                           text[raise_verb.end():trigger.start()], maxsplit=1, flags=re.I)[0]
        if not _FUNDING_CONTEXT.fullmatch(context) or _FUNDING_DEBT.search(context):
            continue
        prior = [m for m in mentions if sentence_start <= m["start"] and m["end"] <= raise_verb.start()]
        if not prior:
            continue
        receiver = prior[-1]
        if (receiver["entity"]["entity_type"] != "ORG"
                or text[sentence_start:receiver["start"]].strip()
                or not _FUNDING_SUBJECT_GAP.fullmatch(text[receiver["end"]:raise_verb.start()])):
            continue
        following = [m for m in mentions if trigger.end() <= m["start"] < sentence_end]
        if not following or not re.fullmatch(r"\s*(?:the\s+)?", text[trigger.end():following[0]["start"]], re.I):
            continue
        investors = [following[0]]
        for investor in following[1:]:
            if not _FUNDING_LIST_GAP.fullmatch(text[investors[-1]["end"]:investor["start"]]):
                break
            investors.append(investor)
        tail = text[investors[-1]["end"]:sentence_end]
        if tail.strip() and not (trigger.group().lower() == "led by"
                                 and re.match(r"\s*,\s*with participation from\b", tail, re.I)):
            continue
        seen = set()
        for investor in investors:
            if investor["entity"]["entity_type"] not in RELATION_TYPES["INVESTED_IN"][0]:
                break
            key = investor["entity"]["entity_id"]
            if key == receiver["entity"]["entity_id"] or key in seen:
                continue
            seen.add(key)
            triple = key, receiver["entity"]["entity_id"]
            if triple in emitted:
                continue
            emitted.add(triple)
            result.append({"subject_id": key, "predicate": "INVESTED_IN",
                           "object_id": receiver["entity"]["entity_id"], "trigger": trigger.group(),
                           "rule_id": "en-INVESTED_IN-funding-round-v1", "assertion_status": "reported"})
    return result
