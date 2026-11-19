"""Resolve explicit round references within a short, uniquely anchored funding context."""
import re

from .entity_quality import entity_name_issue, indirect_organization_reference, named_head
from .schema import stable_id

_RAISED = re.compile(
    r"\b(?:raised|secured|closed)\s+(?:(?:an?|over|more than|nearly|about|approximately|roughly|another)\s+)?"
    r"(?:US\$|[$£€])?\d[\d,.]*|"
    r"\b(?:announced(?: on (?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))?|is backed by)"
    r"\s+(?:(?:a|an|another)\s+)?(?:US\$|[$£€])\d[\d,.]*", re.I)
_EQUITY = re.compile(r"\b(?:series\s+[a-z]\d?|seed (?:round|funding)|equity|funding round|financing round)\b", re.I)
_GENERIC_FUNDING = re.compile(r"\bfunding\b", re.I)
_NON_EQUITY = re.compile(r"\b(?:debt|loans?|grants?|credit facility|non-dilutive|convertible)\b", re.I)
_ROUND_LEAD = re.compile(r"\bround\s+(?:(?:co-)?led by|with participation from)\b", re.I)
_UNCERTAIN = re.compile(r"\b(?:not|never|denied|plans|hopes|seeks|seeking|could|might|may|expected|talks|reportedly)\b", re.I)
_LEAD = re.compile(r"^\s*(?:the|this)\s+(?:round|financing|funding)\b.{0,160}?\bled by\s+(?P<names>.+)", re.I)
_INVESTORS = re.compile(
    r"^\s*(?:(?:other|its)\s+)?investors\s+(?:in\s+(?:this|the)\s+round\s+)?"
    r"(?:include[ds]?|were)\s+(?P<names>.+)", re.I)
_INLINE = re.compile(
    r"\b(?:round|financing|investment|series\s+[a-z]\d?|seed)\b.{0,90}?"
    r"\b(?:led by|with participation from)\s+(?P<names>.+)", re.I)
_CORPORATE_SUFFIX = re.compile(
    r"\S.+\s(?:Capital|Ventures|Partners|Holdings|Bank|Technologies|Labs|Robotics|"
    r"Therapeutics|Corporation|Company|Group|Fund|Management|Investments|Investment Authority|"
    r"Inc\.?|Ltd\.?|LLC|LP|L\.P\.)$")


def funding_references(text, document_id, sentence_rows, mentions, entities, *, name_index=None):
    """Return evidence windows, new typed names, and investor→recipient claims; never use co-occurrence alone."""
    if not _RAISED.search(text):
        return {"entities": [], "sentences": [], "mentions": [], "claims": []}
    by_name = name_index
    if by_name is None:
        by_name = {}
        for entity in entities.values():
            by_name.setdefault(entity["name"].casefold(), []).append(entity)
    local_ids = {row["entity_id"] for row in mentions}
    new_entities, windows, window_mentions, claims = {}, {}, {}, {}
    existing_sids = {row.get("sentence_id") or stable_id(document_id, str(row["start"]), row["text"])
                     for row in sentence_rows}
    existing_mids = {row["mention_id"] for row in mentions if row.get("mention_id")}
    anchor = None
    for index, sentence in enumerate(sentence_rows):
        body = sentence["text"]
        announcement = _RAISED.search(body)
        if announcement:
            anchor = None
            equity = bool(_EQUITY.search(body) or (_ROUND_LEAD.search(body) and not _NON_EQUITY.search(body)))
            generic = bool(_GENERIC_FUNDING.search(body)) and not _NON_EQUITY.search(body)
            if _UNCERTAIN.search(body) or not (equity or generic) or len(list(_RAISED.finditer(body))) != 1:
                continue
            if re.match(r"announced|is backed by", announcement.group(), re.I) and not equity:
                continue
            candidates = {row["entity_id"] for row in mentions
                          if sentence["start"] <= row["start"] < row["end"] <= sentence["start"] + announcement.start()
                          and entities[row["entity_id"]]["entity_type"] == "ORG"
                          and not indirect_organization_reference(text, row["start"])
                          and not entity_name_issue(entities[row["entity_id"]]["name"], "ORG")}
            anchor_sentence = sentence
            if (not candidates and index > 0
                    and not re.search(r"\b(?:company|startup|firm) behind\b", body[:announcement.start()], re.I)
                    and re.match(
                    r"^(?:On (?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s*)?"
                    r"the (?:company|startup|firm)\b", body, re.I)):
                previous = sentence_rows[index - 1]
                if not re.search(r"\n\s*\n", text[previous["end"]:sentence["start"]]):
                    candidates = {row["entity_id"] for row in mentions
                                  if previous["start"] <= row["start"] < row["end"] <= previous["end"]
                                  and entities[row["entity_id"]]["entity_type"] == "ORG"
                                  and not entity_name_issue(entities[row["entity_id"]]["name"], "ORG")}
                    if len(candidates) == 1:
                        recipient_id = next(iter(candidates))
                        references = [row for row in mentions if row["entity_id"] == recipient_id
                                      and previous["start"] <= row["start"] < row["end"] <= previous["end"]]
                        subject_or_introduction = any(
                            not text[previous["start"]:row["start"]].strip()
                            or re.search(r"\b(?:startup|company|firm|platform|launch(?:ed)?|founded|started|named|called)"
                                         r"(?:\s+like)?[: ]\s*$", text[previous["start"]:row["start"]], re.I)
                            or re.match(r"\s+is (?:an?|the) (?:[\w-]+\s+){0,5}(?:startup|company|firm)\b",
                                        text[row["end"]:previous["end"]], re.I)
                            for row in references)
                        if (not subject_or_introduction or _LEAD.match(previous["text"])
                                or _INVESTORS.match(previous["text"])
                                or re.search(r"\b(?:invested|backed|co-led|led)\b", previous["text"], re.I)):
                            candidates = set()
                    anchor_sentence = previous
            if len(candidates) == 1:
                recipient = next(iter(candidates))
                anchor = (index, anchor_sentence, recipient, equity)
        if anchor is None or index - anchor[0] > 4 or sentence["end"] - anchor[1]["start"] > 1800:
            anchor = None
            continue
        listing = ((_INLINE.search(body, announcement.end()) if announcement else None)
                   or _LEAD.search(body) or _INVESTORS.search(body))
        if not listing or _UNCERTAIN.search(body):
            continue
        if (not anchor[3] and not _INVESTORS.match(body)
                or re.match(r"^\s*Its\s+investors\b", body, re.I) and index != anchor[0] + 1):
            continue
        names = listing.group("names")
        names = re.sub(r"\s+with participation from\s+", ", ", names, flags=re.I)
        names = re.split(
            r"(?:^|[,;]\s*|\s+and\s+)(?:operators|employees|executives|founders|individuals|"
            r"angels|people|alumni|partners)\s+(?:from|at|of)\b", names, maxsplit=1, flags=re.I)[0]
        # An explicit list can contain a manager description; the manager is not another investor.
        for part in re.split(r",\s*|\s+and\s+(?=[A-Z])", names):
            part = re.sub(r"^(?:and|&)\s+", "", part.strip())
            name = re.split(r"\s+(?:managed by|which|who|that|with|provided|said|as|at|to|for)\b", part, maxsplit=1)[0]
            name = name.strip().rstrip(".").strip()
            name = named_head(name)
            known = by_name.get(name.casefold(), [])
            known = [row for row in known if row["entity_type"] in {"ORG", "PERSON"}]
            local = [row for row in known if row["entity_id"] in local_ids]
            if local:
                known = local
            elif len(known) > 1 and _CORPORATE_SUFFIX.fullmatch(name):
                known = [row for row in known if row["entity_type"] == "ORG"]
            kind = known[0]["entity_type"] if len(known) == 1 else "ORG"
            if entity_name_issue(name, kind, curated=len(known) == 1 and known[0].get("resolution_method") == "curated_alias"):
                continue
            if len(known) == 1:
                investor = known[0]
            elif not known and _CORPORATE_SUFFIX.fullmatch(name):
                investor = {"entity_id": stable_id("ORG", name.casefold()), "name": name,
                            "entity_type": "ORG", "resolution_method": "exact_surface_type"}
                new_entities[investor["entity_id"]] = investor
                by_name.setdefault(name.casefold(), []).append(investor)
            else:
                continue
            if investor["entity_id"] == anchor[2]:
                continue
            position = body.find(name, listing.start("names"))
            recipient_mentions = [row for row in mentions if row["entity_id"] == anchor[2]
                                  and anchor[1]["start"] <= row["start"] < row["end"] <= anchor[1]["end"]]
            if position < 0 or not recipient_mentions:
                continue
            start, end = anchor[1]["start"], sentence["end"]
            evidence = text[start:end]
            sid = stable_id(document_id, str(start), evidence)
            if sid not in existing_sids:
                windows[sid] = {"sentence_id": sid, "document_id": document_id, "start": start,
                                "end": end, "text": evidence}
            for entity, left, right in [(investor, sentence["start"] + position,
                                         sentence["start"] + position + len(name)),
                                        (entities[anchor[2]], recipient_mentions[0]["start"],
                                         recipient_mentions[0]["end"])]:
                mid = stable_id(sid, str(left), str(right))
                if mid in existing_mids:
                    continue
                window_mentions[mid] = {"mention_id": mid, "sentence_id": sid, "document_id": document_id,
                                        "entity_id": entity["entity_id"], "entity_type": entity["entity_type"],
                                        "surface": text[left:right], "start": left, "end": right,
                                        "method": "explicit_round_reference"}
            event_id = stable_id(investor["entity_id"], "INVESTED_IN", anchor[2], "reported", document_id)
            claim_id = stable_id(event_id, sid)
            claims[claim_id] = {"subject_id": investor["entity_id"], "object_id": anchor[2],
                                "predicate": "INVESTED_IN", "assertion_status": "reported", "event_date": "",
                                "claim_id": claim_id, "event_id": event_id, "document_id": document_id,
                                "sentence_id": sid, "evidence": evidence, "evidence_start": start,
                                "evidence_end": end, "trigger": listing.group(0), "review_status": "unreviewed",
                                "rule_id": ("en-explicit-round-reference-v1" if anchor[3]
                                            else "en-explicit-investor-reference-v1")}
    return {"entities": list(new_entities.values()), "sentences": list(windows.values()),
            "mentions": list(window_mentions.values()), "claims": list(claims.values())}
