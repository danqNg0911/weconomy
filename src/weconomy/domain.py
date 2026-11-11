"""Transparent routing heuristic for the international business assignment."""

import re
import unicodedata

DOMAIN_VERSION = "international_business_assignment_v1"
_SCOPE = DOMAIN_VERSION


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value).casefold().replace("đ", "d")
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


_RULES = (
    ("executive_or_founder", r"\b(?:ceo|chief\s+executive|founder|nha\s+sang\s+lap|giam\s+doc\s+dieu\s+hanh)\b"),
    ("startup", r"\b(?:startups?|khoi\s+nghiep)\b"),
    ("venture_capital", r"\b(?:vc|venture\s+capital|quy\s+dau\s+tu\s+mao\s+hiem)\b"),
    ("billionaire", r"\b(?:billionaires?|ty\s+phu)\b"),
    ("multinational", r"\b(?:multinationals?|da\s+quoc\s+gia)\b"),
    ("antitrust", r"\b(?:antitrust|competition\s+law|chong\s+doc\s+quyen)\b"),
    ("supply_chain", r"\b(?:supply\s+chains?|chuoi\s+cung\s+ung)\b"),
)
_ACTOR = re.compile(
    r"\b(?:companies|company|corporations?|firms?|banks?|cong\s+ty|tap\s+doan|"
    r"investment\s+funds?|hedge\s+funds?|private\s+equity\s+funds?|venture\s+funds?|"
    r"quy\s+dau\s+tu|quy\s+mao\s+hiem)\b"
)
_TRANSACTION = re.compile(
    r"\b(?:invest(?:s|ment|ments|ing|ed)?|dau\s+tu|acquisitions?|acquir(?:e|es|ed|ing)|"
    r"mergers?|merg(?:e|es|ed|ing)|partnerships?|partners|supply|antitrust|competition\s+law|"
    r"thau\s+tom|sap\s+nhap|mua\s+lai|rot\s+von|hop\s+tac|doi\s+tac|cung\s+ung)\b"
)


def classify(title: str, text: str, language: str) -> dict:
    """Classify assignment relevance; this heuristic is not validated for precision."""
    del language  # The normalized cues are language-independent.
    content = _normalize(f"{title or ''}\n{text or ''}")
    reasons = [name for name, pattern in _RULES if re.search(pattern, content)]
    actor_match = _ACTOR.search(content)
    transaction_matches = _TRANSACTION.finditer(content)
    if actor_match and any(
        actor_match.end() <= transaction.start()
        or transaction.end() <= actor_match.start()
        for transaction in transaction_matches
    ):
        reasons.append("corporate_actor_transaction")
    return {"in_scope": bool(reasons), "reasons": reasons, "scope": _SCOPE}
