"""Evidence-preserving projections of verified claims; never part of direct-triple targets."""
from collections import defaultdict
from itertools import combinations

from .schema import stable_id


def shared_investment_targets(claims, entities, articles):
    """A and B share a target; this does not establish partnership or a common funding round.

    Inputs must come from a verified snapshot, not raw model predictions. PRODUCT/PROJECT
    targets are supported for independently verified inputs, without relabeling them ORG.
    """
    entities = {row["entity_id"]: row for row in entities}
    articles = {row["document_id"]: row for row in articles}
    groups = defaultdict(lambda: defaultdict(dict))
    for claim in claims:
        if (claim.get("predicate") != "INVESTED_IN" or claim.get("assertion_status") != "reported"
                or claim.get("review_status") in {"rejected", "incorrect"}):
            continue
        actor, target = entities.get(claim.get("subject_id")), entities.get(claim.get("object_id"))
        article = articles.get(claim.get("document_id"))
        evidence, start, end = claim.get("evidence"), claim.get("evidence_start"), claim.get("evidence_end")
        if (not actor or not target or not article or actor["entity_id"] == target["entity_id"]
                or actor.get("entity_type") not in {"ORG", "PERSON", "GOV"}
                or target.get("entity_type") not in {"ORG", "PRODUCT", "PROJECT"}
                or not claim.get("claim_id") or not evidence or not isinstance(start, int)
                or not isinstance(end, int) or not 0 <= start < end <= len(article["text"])
                or article["text"][start:end] != evidence):
            continue
        groups[target["entity_id"]][actor["entity_id"]][claim["claim_id"]] = claim
    result = []
    for target_id, investors in sorted(groups.items()):
        for left, right in combinations(sorted(investors), 2):
            supporting = sorted([*investors[left].values(), *investors[right].values()],
                                key=lambda row: row["claim_id"])
            result.append({
                "projection_id": stable_id("SHARES_INVESTMENT_TARGET", left, right, target_id),
                "subject_id": left, "subject_name": entities[left]["name"],
                "predicate": "SHARES_INVESTMENT_TARGET",
                "object_id": right, "object_name": entities[right]["name"],
                "target_id": target_id, "target_name": entities[target_id]["name"],
                "target_type": entities[target_id]["entity_type"],
                "derived": True, "rule_id": "two-verified-investments-same-target-v1",
                "same_round_verified": False,
                "supporting_claim_ids": [row["claim_id"] for row in supporting],
                "supporting_evidence": [{"claim_id": row["claim_id"], "investor_id": row["subject_id"],
                    "document_id": row["document_id"], "evidence": row["evidence"],
                    "evidence_start": row["evidence_start"], "evidence_end": row["evidence_end"],
                    "source_url": articles[row["document_id"]].get("canonical_url", "")}
                    for row in supporting],
            })
    return result
