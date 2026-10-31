"""Complete-sentence labels measure false negatives as well as false positives."""
import json
import math
import random
from collections import Counter
from pathlib import Path

from .pipeline import read_table
from .schema import RELATION_TYPES


def write_new_json(path, payload):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)


def annotation_tasks(run, output, limit=200, seed=42):
    sentences = read_table(run, "sentences")
    docs = {d["document_id"]: d for d in read_table(run, "bronze")}
    languages = {a["document_id"]: a["language"] for a in read_table(run, "articles")}
    # Sample all sentences, including those with zero predictions. Hide predictions to reduce anchoring.
    random.Random(seed).shuffle(sentences)
    tasks = [{"sentence_id": s["sentence_id"], "document_id": s["document_id"], "text": s["text"],
              "url": docs[s["document_id"]]["url"], "language": languages[s["document_id"]],
              "split": "pilot", "reviewer": "", "complete": False, "relations": [], "entities": []}
             for s in sentences[:limit]]
    write_new_json(output, {"format": "weconomy-labels-v1", "seed": seed, "tasks": tasks})
    return {"tasks": len(tasks), "output": str(output)}


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
    # Wilson 95% interval, normal approximation to score interval for precision.
    n, z = tp + fp, 1.96
    interval = None
    if n:
        center = (p + z*z / (2*n)) / (1 + z*z/n)
        half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
        interval = [max(0, center-half), min(1, center+half)]
    return {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f,
            "precision_wilson_95": interval}


def evaluate(run, labels):
    payload = json.loads(Path(labels).read_text(encoding="utf-8"))
    tasks = payload["tasks"]
    sentence_rows = {s["sentence_id"]: s for s in read_table(run, "sentences")}
    predictions = read_table(run, "relations")
    mentions = read_table(run, "mentions")
    gold, predicted, gold_ner, predicted_ner = set(), set(), set(), set()
    ids = set()
    for task in tasks:
        sid = task["sentence_id"]
        if sid in ids:
            raise ValueError("Duplicate sentence in labels")
        ids.add(sid)
        if not task.get("complete") or not task.get("reviewer"):
            raise ValueError("Every evaluation sentence needs a reviewer and exhaustive complete=true labels")
        if sid not in sentence_rows or sentence_rows[sid]["text"] != task["text"]:
            raise ValueError("Labels do not match this run's sentence IDs/text")
        for relation in task["relations"]:
            if relation["predicate"] not in RELATION_TYPES:
                raise ValueError("Unknown relation label")
            gold.add((sid, relation["subject_id"], relation["predicate"], relation["object_id"]))
        for entity in task["entities"]:
            start, end = entity["start"], entity["end"]
            if not 0 <= start < end <= len(task["text"]) or task["text"][start:end] != entity["surface"]:
                raise ValueError("Invalid entity label offsets")
            gold_ner.add((sid, start, end, entity["entity_type"]))
    for row in predictions:
        if row["sentence_id"] in ids:
            predicted.add((row["sentence_id"], row["subject_id"], row["predicate"], row["object_id"]))
    for row in mentions:
        sid = row["sentence_id"]
        if sid in ids:
            base = sentence_rows[sid]["start"]
            predicted_ner.add((sid, row["start"] - base, row["end"] - base, row["entity_type"]))
    by_type = {}
    for predicate in RELATION_TYPES:
        g = {r for r in gold if r[2] == predicate}
        p = {r for r in predicted if r[2] == predicate}
        by_type[predicate] = prf(len(g & p), len(p - g), len(g - p))
    return {"sentences": len(ids), "relation": prf(len(gold & predicted), len(predicted-gold), len(gold-predicted)),
            "ner_exact_span": prf(len(gold_ner & predicted_ner), len(predicted_ner-gold_ner),
                                  len(gold_ner-predicted_ner)), "by_type": by_type,
            "splits": dict(Counter(t.get("split", "unspecified") for t in tasks)),
            "warning": "Pilot labels and same-author review cannot establish held-out production precision"}


def validate(run):
    tables = {name: read_table(run, name) for name in
              ("bronze", "articles", "sentences", "mentions", "entities", "events", "relations")}
    documents = {a["document_id"]: a for a in tables["articles"]}
    sentences = {s["sentence_id"]: s for s in tables["sentences"]}
    entities = {e["entity_id"]: e for e in tables["entities"]}
    events = {e["event_id"]: e for e in tables["events"]}
    bronze_ids = {d["document_id"] for d in tables["bronze"]}
    sentence_entities = {}
    for mention in tables["mentions"]:
        sentence_entities.setdefault(mention["sentence_id"], set()).add(mention["entity_id"])
    failures = []
    for name, rows in tables.items():
        key = {"bronze": "document_id", "articles": "document_id", "sentences": "sentence_id",
               "mentions": "mention_id", "entities": "entity_id", "events": "event_id",
               "relations": "claim_id"}[name]
        if len(rows) != len({row[key] for row in rows}):
            failures.append(f"Duplicate primary key: {name}")
    for sentence in tables["sentences"]:
        article = documents.get(sentence["document_id"])
        if (not article or not 0 <= sentence["start"] < sentence["end"] <= len(article["text"])
                or article["text"][sentence["start"]:sentence["end"]] != sentence["text"]):
            failures.append(f"Invalid sentence offsets: {sentence['sentence_id']}")
    for article in tables["articles"]:
        if article["document_id"] not in bronze_ids:
            failures.append(f"Missing bronze snapshot: {article['document_id']}")
    for mention in tables["mentions"]:
        article = documents.get(mention["document_id"])
        if (not article or mention["entity_id"] not in entities or mention["sentence_id"] not in sentences
                or article["text"][mention["start"]:mention["end"]] != mention["surface"]):
            failures.append(f"Invalid mention: {mention['mention_id']}")
        elif not (sentences[mention["sentence_id"]]["document_id"] == mention["document_id"] and
                  sentences[mention["sentence_id"]]["start"] <= mention["start"] < mention["end"]
                  <= sentences[mention["sentence_id"]]["end"]):
            failures.append(f"Mention escapes sentence: {mention['mention_id']}")
    for claim in tables["relations"]:
        article = documents.get(claim["document_id"])
        if (not article or claim["event_id"] not in events or claim["subject_id"] not in entities
                or claim["object_id"] not in entities or claim["sentence_id"] not in sentences
                or article["text"][claim["evidence_start"]:claim["evidence_end"]] != claim["evidence"]):
            failures.append(f"Invalid claim provenance: {claim['claim_id']}")
        if claim["predicate"] not in RELATION_TYPES:
            failures.append(f"Invalid predicate: {claim['claim_id']}")
        elif claim["subject_id"] in entities and claim["object_id"] in entities:
            stypes, otypes = RELATION_TYPES[claim["predicate"]]
            if (entities[claim["subject_id"]]["entity_type"] not in stypes or
                    entities[claim["object_id"]]["entity_type"] not in otypes):
                failures.append(f"Invalid relation endpoint types: {claim['claim_id']}")
        if not {claim["subject_id"], claim["object_id"]} <= sentence_entities.get(claim["sentence_id"], set()):
            failures.append(f"Claim endpoints absent from evidence sentence: {claim['claim_id']}")
        event = events.get(claim["event_id"])
        if event and any(event[k] != claim[k] for k in ("subject_id", "predicate", "object_id", "assertion_status")):
            failures.append(f"Event/claim mismatch: {claim['claim_id']}")
        sentence = sentences.get(claim["sentence_id"])
        if sentence and (sentence["document_id"] != claim["document_id"] or
                         sentence["text"] != claim["evidence"] or
                         sentence["start"] != claim["evidence_start"] or sentence["end"] != claim["evidence_end"]):
            failures.append(f"Claim/sentence mismatch: {claim['claim_id']}")
    return {"valid": not failures, "failures": failures, "counts": {k: len(v) for k, v in tables.items()}}
