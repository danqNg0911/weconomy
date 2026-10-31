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
                spans += [(e.start_char, e.end_char, mapping[e.label_], "spacy")
                          for e in self.en(text).ents if e.label_ in mapping]
            else:
                # Reconstruct offsets against the original sentence, never the tokenizer's joined text.
                cursor, active = 0, None
                for token, _, _, tag in self.vi_ner(text):
                    token = token.replace("_", " ")
                    start = text.find(token, cursor)
                    if start < 0:
                        raise ValueError("underthesea token offsets cannot be aligned")
                    end = start + len(token)
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


# Exact between-mention patterns avoid sentence-wide co-occurrence edges.
RULES = {
    "en": {
        "ACQUIRED": r"(?:has |had )?(?:acquired|bought|purchased|buys|acquires)",
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
        "INVESTED_IN": r"(?:đã )?đầu tư vào",
        "MERGED_WITH": r"(?:đã )?sáp nhập với",
        "SUED": r"(?:đã )?kiện",
        "PARTNERED_WITH": r"(?:đã )?hợp tác với",
        "SUPPLIES_TO": r"cung cấp (?:linh kiện |chip )?cho",
        "CEO_OF": r"là (?:CEO|giám đốc điều hành) của",
        "FOUNDED": r"(?:đã )?(?:đồng )?thành lập",
        "SUBSIDIARY_OF": r"là công ty con của",
        "REGULATES": r"quản lý hoạt động của",
    },
}
NEGATIVE = re.compile(
    r"\b(?:not|never|no|denied|denies|if|whether|rumou?r(?:ed)?|reportedly|allegedly|"
    r"không|chưa|phủ nhận|nếu|liệu|tin đồn)\b", re.I
)


def extract_relations(text, mentions, language):
    # Exclude headline fragments: a headline can compress a proposed deal into a completed-looking verb.
    if not text.endswith((".", "!")) or language not in RULES or NEGATIVE.search(text):
        return []
    # shortcut: quoted statements and hypothetical tense abstain until attribution parsing exists.
    if any(char in text for char in ['"', '“', '”', '?']):
        return []
    result = []
    for left, right in zip(mentions, mentions[1:]):
        gap = text[left["end"]:right["start"]].strip()
        if len(gap) > 120 or left["entity"]["entity_id"] == right["entity"]["entity_id"]:
            continue
        for predicate, pattern in RULES[language].items():
            if not re.fullmatch(pattern, gap, flags=re.I):
                continue
            subjects, objects = RELATION_TYPES[predicate]
            if left["entity"]["entity_type"] not in subjects or right["entity"]["entity_type"] not in objects:
                continue
            result.append({"subject_id": left["entity"]["entity_id"], "predicate": predicate,
                           "object_id": right["entity"]["entity_id"], "trigger": gap,
                           "rule_id": f"{language}-{predicate}-v1", "assertion_status": "reported"})
    return result
