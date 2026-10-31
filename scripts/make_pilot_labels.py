"""Agent's explicit pilot annotations of the four real excerpts; NOT independent gold.

No prediction file is read. This deterministic transcription makes the pilot review reproducible.
Use two human reviewers and an unseen corpus before making quality claims.
"""
import argparse
import json
from pathlib import Path

from weconomy.pipeline import read_table
from weconomy.schema import stable_id

# Explicit span labels in corpus sentence order after the decimal-safe splitter.
ENTITIES = {
    0: [("Disney", "ORG"), ("Pixar", "ORG")],
    1: [("The Walt Disney Company", "ORG"), ("Pixar", "ORG")],
    2: [("Steve Jobs", "PERSON"), ("Pixar", "ORG"), ("Apple", "ORG"), ("Disney", "ORG")],
    3: [("Microsoft", "ORG")],
    4: [("Microsoft", "ORG"), ("Medstory", "ORG")],
    5: [],
    6: [("Medstory", "ORG")],
    7: [("Medstory", "ORG")],
    # The source explicitly calls Azyxxi a system, not a company. Exclude this product from ORG gold.
    8: [("Microsoft", "ORG")],
    9: [], 10: [],
    11: [("Microsoft", "ORG"), ("GitHub", "ORG")],
    12: [("US", "PLACE"), ("Microsoft", "ORG"), ("GitHub", "ORG")],
    13: [("Microsoft", "ORG"), ("Nat Friedman", "PERSON"), ("GitHub", "ORG")],
    14: [("Microsoft", "ORG"), ("GitHub", "ORG")],
    15: [("European Union", "GOV")],
    16: [("Microsoft", "ORG")],
    17: [("Microsoft", "ORG")],
    18: [("Microsoft", "ORG"), ("Hoa Kỳ", "PLACE"), ("Redmond", "PLACE"), ("Washington", "PLACE")],
    19: [("Bill Gates", "PERSON"), ("Paul Allen", "PERSON")],
    20: [("MITS", "ORG")],
    21: [("Paul Allen", "PERSON"), ("Bill Gates", "PERSON"), ("Microsoft", "ORG"), ("Gates", "PERSON")],
    22: [("Allen", "PERSON"), ("Microsoft", "ORG")],
}
RELATIONS = {
    2: [("Steve Jobs", "PERSON", "CEO_OF", "Pixar", "ORG"),
        ("Steve Jobs", "PERSON", "CEO_OF", "Apple", "ORG")],
    12: [("Microsoft", "ORG", "ACQUIRED", "GitHub", "ORG")],
    21: [("Paul Allen", "PERSON", "FOUNDED", "Microsoft", "ORG"),
         ("Bill Gates", "PERSON", "FOUNDED", "Microsoft", "ORG")],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = read_table(args.run, "sentences")
    if len(rows) != 23 or rows[8]["text"] != "In 2006 Microsoft bought Azyxxi, which is a clinical health care service system.":
        raise ValueError("Pilot annotations apply only to the reviewed excerpt corpus/segmenter")
    tasks = []
    for index, sentence in enumerate(rows):
        spans, cursor = [], 0
        for surface, entity_type in ENTITIES[index]:
            start = sentence["text"].find(surface, cursor)
            if start < 0:
                raise ValueError(f"Label cannot align: sentence {index}: {surface}")
            end = start + len(surface)
            spans.append({"surface": surface, "start": start, "end": end, "entity_type": entity_type})
            cursor = end
        relations = []
        for subject, stype, predicate, obj, otype in RELATIONS.get(index, []):
            relations.append({"subject_id": stable_id(stype, subject.casefold()), "predicate": predicate,
                              "object_id": stable_id(otype, obj.casefold())})
        tasks.append({"sentence_id": sentence["sentence_id"], "document_id": sentence["document_id"],
                      "text": sentence["text"], "complete": True, "reviewer": "agent-pilot-not-independent",
                      "split": "pilot", "entities": spans, "relations": relations})
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump({"format": "weconomy-labels-v1", "warning": "Agent pilot labels, NOT human held-out gold",
                   "guidelines": "docs/ANNOTATION.md", "tasks": tasks}, stream, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
