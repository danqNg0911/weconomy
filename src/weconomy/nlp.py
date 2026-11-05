"""Deterministic baseline plus optional bilingual GLiNER extraction."""
import re
import unicodedata
from pathlib import Path

import yaml
from langdetect import DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from rapidfuzz import fuzz

from .schema import RELATION_TYPES, stable_id

DetectorFactory.seed = 0


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
    # shortcut: abbreviations still need a model segmenter; decimal numbers must remain intact.
    start = 0
    for match in re.finditer(r"[.!?]+(?=\s|$)|\n+|$", text):
        # Keep common abbreviations inside a continuing sentence, e.g. "the U.S. military".
        tail = text[match.end():].lstrip()
        prefix = text[:match.end()]
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

    def resolve(self, surface, entity_type):
        key = normalize(surface).casefold()
        name, kind = self.aliases.get(key, (normalize(surface), entity_type))
        method = "curated_alias" if key in self.aliases else "exact_surface_type"
        return {"entity_id": stable_id(kind, name.casefold()), "name": name,
                "entity_type": kind, "resolution_method": method}

    def suggestions(self, surface, threshold=90):
        # Fuzzy matches are review suggestions; they never auto-merge entities.
        return [{"alias": alias, "score": fuzz.ratio(surface.casefold(), alias)}
                for alias in self.aliases if fuzz.ratio(surface.casefold(), alias) >= threshold]

    def mentions(self, text, language):
        if language not in {"vi", "en"}:
            return []
        spans = [(m.start(), m.end(), "", "gazetteer") for m in self.alias_pattern.finditer(text)]
        if self.backend == "models":
            entities, relations = self._infer(text, language)
            self._prediction = (text, language, entities, relations)
            for row in entities:
                start, end = row["start"], row["end"]
                kind = self._entity_type(row["label"], language)
                if kind and 0 <= start < end <= len(text) and text[start:end] == row["text"]:
                    spans.append((start, end, kind, "gliner"))
        # Keep longest span at each overlap; seeds win equal spans.
        chosen = []
        for start, end, kind, method in sorted(
                spans, key=lambda x: (x[3] != "gazetteer", -(x[1] - x[0]), x[0])):
            if any(start < b and end > a for a, b, *_ in chosen):
                continue
            chosen.append((start, end, kind, method))
        result = []
        for start, end, kind, method in sorted(chosen):
            entity = self.resolve(text[start:end], kind or "ORG")
            result.append({"start": start, "end": end, "surface": text[start:end], "method": method,
                           "entity": entity})
        return result

    def relations(self, text, mentions, language):
        result = extract_relations(text, mentions, language)
        if self.backend == "models" and language in self.models and relation_sentence(text, language):
            if not self._prediction or self._prediction[:2] != (text, language):
                entities, relations = self._infer(text, language)
            else:
                _, _, entities, relations = self._prediction
            by_span = {(m["start"], m["end"]): m for m in mentions}
            for row in relations:
                predicate = self._predicate(row["relation"], language)
                head, tail = row["head"], row["tail"]
                subject, object_ = by_span.get((head["start"], head["end"])), by_span.get(
                    (tail["start"], tail["end"]))
                if not predicate or not subject or not object_:
                    continue
                if subject["entity"]["entity_id"] == object_["entity"]["entity_id"]:
                    continue
                constraints = RELATION_TYPES.get(predicate)
                if constraints and (subject["entity"]["entity_type"] not in constraints[0]
                                    or object_["entity"]["entity_type"] not in constraints[1]):
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
            texts=[text], labels=ENTITY_LABELS[language], relations=list(RELATION_LABELS[language]),
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
        "HONORS": r"(?:đã )?vinh danh",
        "LAUNCHES": r"(?:đã )?ra mắt",
        "APPOINTS": r"(?:đã )?bổ nhiệm",
    },
}
NEGATIVE = re.compile(
    r"\b(?:not|never|no|denied|denies|if|whether|rumou?r(?:ed)?|reportedly|allegedly|"
    r"không|chưa|phủ nhận|nếu|tin đồn)\b", re.I
)
VI_UNCERTAIN = re.compile(r"(?:^\s*liệu\b|\b(?:chưa rõ|không biết|cân nhắc|xem xét)\s+liệu\b)", re.I)

# These patterns have the opposite surface order from the graph edge.
REVERSE_RULES = {
    "en": {
        "ACQUIRED": r"(?:was|has been|had been) (?:acquired|bought|purchased) by",
        "SUED": r"(?:was|has been) sued by",
        "FOUNDED": r"(?:was|has been) (?:co-)?founded by",
    },
    "vi": {
        "ACQUIRED": r"(?:đã )?được mua lại bởi",
        "SUED": r"(?:đã )?bị kiện bởi",
        "FOUNDED": r"(?:đã )?được (?:đồng )?thành lập bởi",
        "HONORS": r"(?:đã )?được vinh danh bởi",
    },
}

ROLE_RULES = {
    "en": [
        ("CEO_OF", r",\s*(?:the )?(?:(?:co-)?founder and )?(?:CEO|chief executive officer) of", False),
        ("FOUNDED", r",\s*(?:the )?(?:co-)?founder(?: and (?:CEO|chief executive officer))? of", False),
        ("CEO_OF", r"(?:[’']s\s+)?(?:(?:co-)?founder and )?(?:CEO|chief executive officer)", True),
        ("FOUNDED", r"(?:[’']s\s+)?(?:co-)?founder(?: and (?:CEO|chief executive officer))?", True),
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


def relation_sentence(text, language, *, allow_quotes=False):
    # Exclude headline fragments: a headline can compress a proposed deal into a completed-looking verb.
    if (not text.endswith((".", "!")) or language not in RULES or NEGATIVE.search(text)
            or (language == "vi" and VI_UNCERTAIN.search(text))):
        return False
    # shortcut: quoted statements and hypothetical tense abstain until attribution parsing exists.
    if '?' in text or (not allow_quotes and any(char in text for char in ['"', '“', '”'])):
        return False
    return True


def extract_relations(text, mentions, language):
    if (not relation_sentence(text, language, allow_quotes=True)
            or re.search(r"\b(?:stake in|shares in|assets)\b", text, re.I)):
        return []
    strict = relation_sentence(text, language)
    result = []
    for left, right in zip(mentions, mentions[1:]):
        gap = text[left["end"]:right["start"]].strip()
        # Buying "GitHub's assets" is not acquiring GitHub; coordinated objects need full parsing.
        coordinated = bool(re.match(r"(?:[’']s\b|\s+(?:and|or|và|hoặc)\b)",
                                    text[right["end"]:], flags=re.I))
        if re.match(r"[’']s\b", text[right["end"]:], flags=re.I):
            continue
        if len(gap) > 120 or left["entity"]["entity_id"] == right["entity"]["entity_id"]:
            continue
        rules = ([(p, pattern, False, False) for p, pattern in RULES[language].items()]
                 + [(p, pattern, True, False) for p, pattern in REVERSE_RULES[language].items()]
                 if not coordinated else []) if strict else []
        if outside_quotes(text, left["start"], right["end"]):
            rules += [(*rule, True) for rule in ROLE_RULES[language]]
        for predicate, pattern, reverse, role_rule in rules:
            if re.search(r"\b(?:stake in|shares in|assets)\b", text, re.I):
                continue
            if not re.fullmatch(pattern, gap, flags=re.I):
                continue
            subject, object_ = (right, left) if reverse else (left, right)
            constraints = RELATION_TYPES.get(predicate)
            if (constraints and (subject["entity"]["entity_type"] not in constraints[0]
                    or object_["entity"]["entity_type"] not in constraints[1])
                    or (role_rule and predicate == "FOUNDED"
                        and subject["entity"]["entity_type"] != "PERSON")):
                continue
            result.append({"subject_id": subject["entity"]["entity_id"], "predicate": predicate,
                           "object_id": object_["entity"]["entity_id"], "trigger": gap,
                           "rule_id": f"{language}-{predicate}-{'reverse' if reverse else 'direct'}-v2",
                           "assertion_status": "agreement_reported" if predicate == "AGREED_TO_ACQUIRE" else "reported"})
    if language == "en" and strict:
        result.extend(funding_round_relations(text, mentions))
    return result


ENTITY_LABELS = {
    "en": {"person": "A person", "organization": "A company or organization",
           "place": "A geographic place"},
    "vi": ["người", "tổ chức", "địa điểm"],
}
ENTITY_TYPES = {
    "en": {"person": "PERSON", "organization": "ORG", "place": "PLACE"},
    "vi": {"người": "PERSON", "tổ chức": "ORG", "địa điểm": "PLACE"},
}
RELATION_LABELS = {
    "en": {
        "acquired": "ACQUIRED", "agreed to acquire": "AGREED_TO_ACQUIRE", "invested in": "INVESTED_IN",
        "merged with": "MERGED_WITH", "sued": "SUED", "partnered with": "PARTNERED_WITH",
        "supplies to": "SUPPLIES_TO", "is ceo of": "CEO_OF", "founded": "FOUNDED",
        "is subsidiary of": "SUBSIDIARY_OF", "regulates": "REGULATES",
    },
    "vi": {
        "mua lại": "ACQUIRED", "đạt thỏa thuận mua lại": "AGREED_TO_ACQUIRE", "đầu tư vào": "INVESTED_IN",
        "sáp nhập với": "MERGED_WITH", "kiện": "SUED", "hợp tác với": "PARTNERED_WITH",
        "cung cấp cho": "SUPPLIES_TO", "là tổng giám đốc của": "CEO_OF", "thành lập": "FOUNDED",
        "là công ty con của": "SUBSIDIARY_OF", "quản lý hoạt động của": "REGULATES",
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
