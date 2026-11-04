"""Deterministic baseline plus optional Vietnamese/English statistical NER."""
import re
import unicodedata
from pathlib import Path

import yaml
from langdetect import DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from rapidfuzz import fuzz

from .schema import RELATION_TYPES, stable_id

DetectorFactory.seed = 0

# Underthesea relocates Vietnamese tone marks in these equivalent spellings (Tuỳ -> Tùy).
# Every replacement is two code points, so source offsets and original surfaces remain unchanged.
VI_TONE_VARIANTS = dict(zip(
    ["oà", "oá", "oả", "oã", "oạ", "oè", "oé", "oẻ", "oẽ", "oẹ", "uỳ", "uý", "uỷ", "uỹ", "uỵ"],
    ["òa", "óa", "ỏa", "õa", "ọa", "òe", "óe", "ỏe", "õe", "ọe", "ùy", "úy", "ủy", "ũy", "ụy"],
))
VI_TONE_PATTERN = re.compile("|".join(VI_TONE_VARIANTS), re.I)


def tone_view(text):
    text = re.sub(r"(?<!\w)qui(?!\w)",
                  lambda m: m.group()[:-1] + ("Y" if m.group()[-1].isupper() else "y"),
                  text, flags=re.I)
    return VI_TONE_PATTERN.sub(lambda m: "".join(
        new.upper() if old.isupper() else new
        for old, new in zip(m.group(), VI_TONE_VARIANTS[m.group().lower()])), text)


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


def align_token(text, token, cursor):
    """Consume in order; allow spacing and equivalent Vietnamese tone placement, keeping source offsets."""
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    for surface in (token, token.replace("_", " ")):
        letters = [re.escape(char) for char in tone_view(unicodedata.normalize("NFC", surface))
                   if not char.isspace()]
        if not letters:
            continue
        matched = re.compile(r"\s*".join(letters)).match(tone_view(text), cursor)
        if matched:
            return matched.span()
    raise ValueError(f"underthesea token offsets cannot be aligned at character {cursor}")


class NLP:
    def __init__(self, config):
        self.backend = config["ner_backend"]
        if self.backend not in {"gazetteer", "models"}:
            raise ValueError("ner_backend must be gazetteer or models")
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
        self.en = None
        self._en_doc = None
        if self.backend == "models":
            import spacy
            import underthesea
            self.vi_ner = underthesea.ner
            self.en = spacy.load(config["english_model"])

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
            if language == "en":
                mapping = {"PERSON": "PERSON", "ORG": "ORG", "GPE": "PLACE", "LOC": "PLACE"}
                self._en_doc = self.en(text)
                spans += [(e.start_char, e.end_char, mapping[e.label_], "spacy")
                          for e in self._en_doc.ents if e.label_ in mapping]
            else:
                # Reconstruct offsets against the original sentence, never the tokenizer's joined text.
                cursor, active = 0, None
                for token, _, _, tag in self.vi_ner(text):
                    start, end = align_token(text, token, cursor)
                    cursor = end
                    kind = {"PER": "PERSON", "ORG": "ORG", "LOC": "PLACE"}.get(tag[2:])
                    if tag.startswith("I-") and active and active[2] == kind:
                        active[1] = end
                    else:
                        if active:
                            spans.append((*active, "underthesea"))
                        active = [start, end, kind] if kind else None
                if active:
                    spans.append((*active, "underthesea"))
        # Keep longest span at each overlap; seeds win equal spans.
        chosen = []
        for start, end, kind, method in sorted(spans, key=lambda x: (-(x[1] - x[0]), x[0])):
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
        if self.backend == "models" and language == "en" and relation_sentence(text, language):
            doc = self._en_doc if self._en_doc is not None and self._en_doc.text == text else self.en(text)
            result += dependency_relations(doc, mentions)
        # A rule and the parser can find the same assertion; keep a single claim per sentence/triple.
        unique = {}
        for claim in result:
            unique.setdefault((claim["subject_id"], claim["predicate"], claim["object_id"]), claim)
        return list(unique.values())


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
        "PARTNERED_WITH": r"(?:đã )?hợp tác với",
        "SUPPLIES_TO": r"cung cấp (?:linh kiện |chip )?cho",
        "CEO_OF": r"là (?:CEO|tổng giám đốc|giám đốc điều hành) của",
        "FOUNDED": r"(?:đã )?(?:đồng )?thành lập",
        "SUBSIDIARY_OF": r"là công ty con của",
        "REGULATES": r"quản lý hoạt động của",
    },
}
NEGATIVE = re.compile(
    r"\b(?:not|never|no|denied|denies|if|whether|rumou?r(?:ed)?|reportedly|allegedly|"
    r"không|chưa|phủ nhận|nếu|liệu|tin đồn)\b", re.I
)

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
    if not text.endswith((".", "!")) or language not in RULES or NEGATIVE.search(text):
        return False
    # shortcut: quoted statements and hypothetical tense abstain until attribution parsing exists.
    if '?' in text or (not allow_quotes and any(char in text for char in ['"', '“', '”'])):
        return False
    return True


def extract_relations(text, mentions, language):
    if not relation_sentence(text, language, allow_quotes=True):
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
            if not re.fullmatch(pattern, gap, flags=re.I):
                continue
            subject, object_ = (right, left) if reverse else (left, right)
            subjects, objects = RELATION_TYPES[predicate]
            if (subject["entity"]["entity_type"] not in subjects
                    or object_["entity"]["entity_type"] not in objects
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


def dependency_relations(doc, mentions):
    """English explicit verb arguments only; never infer endpoints from pronouns or co-occurrence."""
    verbs = {"acquire": ("ACQUIRED", None), "buy": ("ACQUIRED", None),
             "purchase": ("ACQUIRED", None), "sue": ("SUED", None), "found": ("FOUNDED", None),
             "invest": ("INVESTED_IN", "in"), "partner": ("PARTNERED_WITH", "with"),
             "merge": ("MERGED_WITH", "with")}

    def endpoint(token):
        found = [m for m in mentions if m["start"] <= token.idx and token.idx + len(token.text) <= m["end"]]
        return found[0] if len(found) == 1 else None

    result = []
    for verb in doc:
        if verb.pos_ != "VERB" or verb.lemma_ not in verbs:
            continue
        children = list(verb.children)
        attributed = (verb.dep_ == "ccomp" and verb.head.dep_ == "ROOT"
                      and verb.head.lemma_ in {"say", "announce", "confirm", "report", "reveal"})
        scope = children + list(verb.head.children) if attributed else children
        # Accept explicit assertions under affirmative reporting verbs, never plans or unresolved pronouns.
        if (verb.dep_ in {"xcomp", "relcl", "advcl", "conj"}
                or (verb.dep_ == "ccomp" and not attributed)
                or any(c.dep_ == "neg" or c.tag_ == "MD" for c in scope)):
            continue
        predicate, prep = verbs[verb.lemma_]
        subjects = [c for c in children if c.dep_ == "nsubj"]
        objects = [c for c in children if c.dep_ == "dobj"] if prep is None else [
            obj for c in children if c.dep_ == "prep" and c.lower_ == prep
            for obj in c.children if obj.dep_ == "pobj"]
        passive = [c for c in children if c.dep_ == "nsubjpass"]
        if passive and prep is None:
            subjects = [obj for c in children if c.dep_ == "agent" and c.lower_ == "by"
                        for obj in c.children if obj.dep_ == "pobj"]
            objects = passive
        if len(subjects) != 1 or len(objects) != 1:
            continue
        if any(list(token.conjuncts) for token in [subjects[0], objects[0]]):
            continue
        subject, object_ = endpoint(subjects[0]), endpoint(objects[0])
        if not subject or not object_ or subject["entity"]["entity_id"] == object_["entity"]["entity_id"]:
            continue
        subject_types, object_types = RELATION_TYPES[predicate]
        if (subject["entity"]["entity_type"] not in subject_types
                or object_["entity"]["entity_type"] not in object_types):
            continue
        result.append({"subject_id": subject["entity"]["entity_id"], "predicate": predicate,
                       "object_id": object_["entity"]["entity_id"], "trigger": verb.text,
                       "rule_id": f"en-{predicate}-dependency{'-attributed' if attributed else ''}-v1",
                       "assertion_status": "reported"})
    return result
