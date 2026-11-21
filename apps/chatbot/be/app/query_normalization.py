"""Small bilingual alias layer; no database writes or additional model calls."""

import unicodedata

from .guards import normalize

# Apply aliases to whole entity names, never to substrings in company names.
ALIASES = (
    ("Mỹ", "Hoa Kỳ", "United States", "United States of America", "USA", "US", "U.S."),
    ("Nhật Bản", "Nhật", "Japan"),
    ("Việt Nam", "Vietnam", "Viet Nam"),
    ("Trung Quốc", "China", "People's Republic of China"),
    ("Hàn Quốc", "South Korea", "Republic of Korea"),
    ("Anh", "Vương quốc Anh", "United Kingdom", "UK"),
    ("Đức", "Germany"),
    ("Pháp", "France"),
    ("Ấn Độ", "India"),
    ("Singapore", "Xin-ga-po"),
    ("Úc", "Australia"),
    ("Thái Lan", "Thailand"),
    ("Đài Loan", "Taiwan"),
    ("Liên minh châu Âu", "European Union", "EU"),
    ("Ngân hàng Thế giới", "World Bank"),
    ("Quỹ Tiền tệ Quốc tế", "International Monetary Fund", "IMF"),
    ("Tổ chức Thương mại Thế giới", "World Trade Organization", "WTO"),
    ("Ngân hàng Phát triển châu Á", "Asian Development Bank", "ADB"),
)
ALIAS_INDEX = {normalize(alias): group for group in ALIASES for alias in group}

# Native Cypher replace/reduce handles Vietnamese accents without requiring APOC
# or changing the existing AuraDB schema. Values are passed as parameters.
FOLDS = [
    [char, normalize(char)]
    for char in map(chr, range(0x00C0, 0x1F00))
    if char.islower()
    and len(normalize(char)) == 1
    and normalize(char) in "abcdefghijklmnopqrstuvwxyz"
    and normalize(char) != char
]


def variants(value, extra=()):
    original = " ".join(unicodedata.normalize("NFKC", value).split())[:120]
    names = [original, *list(extra)[:4]]
    names.extend(ALIAS_INDEX.get(normalize(original), ()))
    return list(dict.fromkeys(normalize(name) for name in names if 2 <= len(name.strip()) <= 120))


def normalize_plan(plan):
    groups = []
    seen = set()
    for original in plan.entities:
        names = variants(original, plan.entity_variants.get(original, []))
        if names and not seen.intersection(names):
            groups.append({"original": original, "variants": names})
            seen.update(names)
    fallback = list(dict.fromkeys(name for term in plan.terms for name in variants(term)))[:20]
    return {"entities": groups, "fallback_terms": fallback}


def partial_terms(names):
    # Country/institution aliases must match whole names: "Nhật" must not link
    # to a person called "Phạm Nhật Vượng" when no Japan node exists.
    return [name for name in names if len(name) >= 4 and name not in ALIAS_INDEX]
