"""Conservative checks shared by extraction and domain verification."""
import re
from collections import defaultdict

from .schema import stable_id

_ROUND = re.compile(
    r"\b(?:pre[-– ]?|post[-– ]?)?series\s+[a-z]\d?\+?"
    r"(?:\s+(?:round|funding|financing|startups?))?$", re.I)
_PRODUCT = re.compile(
    r"^(?:chatgpt|gpt[- ]?\d[\w. -]*|model\s+[sxy\d]+|iphone\s*\d[\w -]*|"
    r"claude\s+\d[\w. -]*|gemini\s+\d[\w. -]*)$", re.I)
_EVENT = re.compile(
    r"\b(?:expo hall|founder summit|startup battlefield|disrupt(?:\s+\d{4})?|"
    r"conference|exhibit table)\b", re.I)
_GENERIC = re.compile(
    r"^(?:(?:the|a|an|this|that|these|those|their|our|its|his|her|một|các|những)\s+)?"
    r"(?:company|companies|business|firm|startup|fund|investor|founder|customer|client|supplier|"
    r"team|organization|government|VCs|LPs|GPs|applications?|industries|utilities|technologies|"
    r"doanh nghiệp|công ty|quỹ|nhà đầu tư|nhà sáng lập|khách hàng|tập đoàn|ngân hàng)s?$", re.I)
_PRONOUNS = {"he", "she", "they", "it", "its", "him", "her", "them", "their", "his", "who",
             "we", "you", "our", "this", "that", "ông", "bà", "họ", "nó", "đây", "đó"}
_NON_NAMES = {"kế hoạch", "mô hình", "báo cáo", "dự án", "thương vụ", "thị trường", "chính sách", "vcs", "evtol"}
_DESCRIBED_NAME = re.compile(
    r"^(?:[A-Za-z][\w-]*\s+){0,6}"
    r"(?:startup|start-up|company|firm|fund|conglomerate)\s+(?P<name>[A-Z][\w’'&. -]*)$")
_VI_DESCRIBED_NAME = re.compile(
    r"^(?i:mạng xã hội|xã hội|công ty|tập đoàn|ngân hàng|quỹ đầu tư)\s+(?P<name>[A-ZÀ-Ỹ][\w’'&. -]*)$")
_OWNED_NAMED_ORGANIZATION = re.compile(
    r"^[A-Z][\w’-]*(?:\s+[A-Z][\w’-]*){0,3}[’']s?\s+(?:company|firm|fund|startup)\s+"
    r"(?P<name>[A-Z][\w’'&. -]*)$")
_GENERIC_GROUP = re.compile(
    r"^(?:(?:[A-Za-z][\w-]*|\d[\d,.]*)\s+){0,7}"
    r"(?:companies|startups|firms|funds|investors|founders|customers|clients|labs|models|products|teams|"
    r"entrepreneurs|family offices|startup|company|firm|fund|therapy|platform|software|service|model)$")
_QUANTIFIED_GROUP = re.compile(
    r"^(?i:multiple|several|many|some|various|other|leading|major|these|those)\s+[a-z][a-z -]*$")
_NAME_CONTINUATION = re.compile(
    r"\s+(?:Foundation|Ventures|Capital|Partners|Management|Labs|Corporation|Company|Group|"
    r"Holdings|Bank|University|Institute|Research)\b")
_GOVERNMENT_NAME = re.compile(
    r"^(?:(?:Ministry|Department) of .+|.+ (?:Commission|Court|Authority)|"
    r"(?:Bộ|Ủy ban) .+)$")


def named_head(surface):
    """Separate an explicit English business descriptor from its following proper name."""
    match = (_DESCRIBED_NAME.fullmatch(surface.strip()) or _VI_DESCRIBED_NAME.fullmatch(surface.strip())
             or _OWNED_NAMED_ORGANIZATION.fullmatch(surface.strip()))
    return match.group("name") if match else surface.strip()


def x_organization_context(text):
    """Resolve the observed homonym only with explicit context; mixed or absent evidence abstains."""
    alphabet = bool(re.search(r"Alphabet[’']s\s+X\b|\bX\s+moonshot factory\b|"
                              r"\bX,\s*Alphabet[’']s\s+[“\"]?moonshot factory", text))
    social = bool(re.search(
        r"(?:Musk[’']s\s+(?:(?:social|media|company|platform)\s+){0,3}|"
        r"social media (?:company|platform)\s+|social network\s+|mạng xã hội\s+)X\b|"
        r"\bX,?\s+(?:formerly|previously known as)\s+Twitter\b|"
        r"\b(?:posted|wrote|announced|said) on X\b", text))
    if alphabet == social:
        return None
    name = "X (Alphabet)" if alphabet else "X (social network)"
    return {"entity_id": stable_id("ORG", name.casefold()), "name": name,
            "entity_type": "ORG", "resolution_method": "explicit_document_context"}


def government_aliases(text):
    """Known agencies require full-name and jurisdiction evidence in this document."""
    if not re.search(r"United States|U\.S\.|Trump administration|Biden administration|Wells Notices?|Clayton Act", text):
        return {}
    agencies = [
        ("United States Securities and Exchange Commission", ["Securities and Exchange Commission"], ["SEC"]),
        ("United States Department of Justice", ["Department of Justice", "Justice Department"], ["DOJ"]),
        ("United States Federal Trade Commission", ["Federal Trade Commission"], ["FTC"]),
    ]
    result = {}
    for name, full_names, abbreviations in agencies:
        if not any(re.search(r"(?<!\w)" + re.escape(full) + r"(?!\w)", text, re.I) for full in full_names):
            continue
        if name.endswith("Securities and Exchange Commission") and "Southeastern Conference" in text:
            abbreviations = []
        for alias in [name, *full_names, *abbreviations]:
            result[alias.casefold()] = {"entity_id": stable_id("GOV", name.casefold()), "name": name,
                                       "entity_type": "GOV", "resolution_method": "document_verified_government_alias"}
    return result


def partial_organization_name(text, end):
    return bool(_NAME_CONTINUATION.match(text[end:]))


def organization_person_role(text, end):
    return bool(re.match(r"(?:[’']s)?\s+(?:(?:co-)?founder|CEO|chief executive officer|"
                         r"chairman|chairwoman|partner|nhà sáng lập|đồng sáng lập|tổng giám đốc)\b",
                         text[end:], re.I))


def possessive_person_reference(text, end):
    return bool(re.match(r"[’']s?(?=\s)", text[end:]))


def historical_role(text, subject, object_):
    """Match historical CEO wording at this endpoint occurrence, not anywhere in the sentence."""
    role = r"(?:CEO|chief executive officer|tổng giám đốc|giám đốc điều hành)"
    former = r"(?:former|ex[- ]|cựu)\s*"
    if object_["end"] <= subject["start"]:
        prefix = text[max(0, object_["start"] - 70):object_["start"]]
        gap = text[object_["end"]:subject["start"]]
        return bool((re.search(r"\b" + former + r"$", prefix, re.I)
                     and re.fullmatch(r"(?:[’']s)?\s+(?:(?:co-)?founder and\s+)?" + role + r"\s+", gap, re.I))
                    or re.fullmatch(r"(?:[’']s)?\s+" + former + role + r"\s+", gap, re.I)
                    or (re.search(r"\b" + former + role + r"\s+(?:(?:of|của|tại)\s+)?$", prefix, re.I)
                        and re.fullmatch(r"\s+", gap)))
    gap = text[subject["end"]:object_["start"]]
    return bool(re.fullmatch(r",?\s+(?:(?:is|was)\s+)?(?:the\s+)?" + former + role
                             + r"\s+(?:of|của|tại)\s+", gap, re.I))


def organization_name_aliases(mentions, names):
    """Resolve a unique corporate expansion among validated ORG spans in one document."""
    ids = {row[2] for row in mentions}
    by_name = defaultdict(set)
    for entity_id in ids:
        by_name[names[entity_id]].add(entity_id)
    result = {}
    for short in ids:
        if len(names[short]) < 4:
            continue
        candidates = {full for suffix in ("Materials", "Enterprises", "Atomics", "Health", "Technologies",
                                          "Inc", "Inc.", "Ltd", "Ltd.")
                      for full in by_name.get(names[short] + " " + suffix, ())}
        if len(candidates) == 1:
            result[short] = next(iter(candidates))
    return result


def indirect_organization_reference(text, start):
    return bool(re.search(
        r"\b(?:(?:subsidiary|division|unit) of|(?:company|startup|firm) behind|"
        r"(?:công ty|doanh nghiệp) đứng sau|"
        r"(?:công ty con|chi nhánh|bộ phận) (?:của|thuộc))\s*$",
        text[max(0, start - 100):start], re.I))


def entity_name_issue(name, entity_type, *, curated=False):
    """Return a reason to quarantine a surface; capitalization alone never proves validity."""
    if curated:
        return None
    name = name.strip()
    if not name or not any(char.isalpha() for char in name):
        return "not_a_name"
    if (name.casefold() in _PRONOUNS | _NON_NAMES or _GENERIC.fullmatch(name)
            or _GENERIC_GROUP.fullmatch(name) or _QUANTIFIED_GROUP.fullmatch(name)):
        return "generic_or_pronominal"
    if entity_type not in {"ORG", "PERSON", "PLACE", "GOV"}:
        return "unsupported_entity_type"
    if entity_type == "ORG":
        if _GOVERNMENT_NAME.fullmatch(name) and not name.endswith("Investment Authority"):
            return "government_requires_type_verification"
        if _ROUND.search(name):
            return "financing_round_not_organization"
        if re.fullmatch(r"fund\s+[ivxlcdm\d]+", name, re.I):
            return "unnamed_fund_vehicle"
        if _PRODUCT.fullmatch(name):
            return "product_not_organization"
        if _EVENT.search(name):
            return "event_not_organization"
    named_part = name.split()[0] if entity_type == "ORG" else name
    if not any(char.isupper() for char in named_part):
        return "lowercase_unverified_name"
    return None
