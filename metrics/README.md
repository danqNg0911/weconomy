# Graph quality evaluation

This folder contains reproducible quality checks for the normalized graph export. It separates full-population
structural/schema checks from sampled accuracy review: a valid evidence link is not proof that an extracted entity or
relation is correct.

## Layout

- `graph_quality.py`: structural audit, fixed-seed review-sample preparation, and scoring.
- `build_strict_candidate.py`: non-destructive graph-contract projection and quarantine export.
- `samples/v15-global-business-only/`: reviewer packets and the export checksums/seed used to produce them.
- `results/`: full-export audit/profile, AI screening results, and, after human review, measured node/relation scores.

The current target is relation-triple precision for the graph. Node precision is measured separately. The edge label
must confirm the in-domain actors, subject/object direction, predicate, event status, and evidence support. The node
label must confirm that the candidate is a correctly named, correctly typed entity in the assignment domain.

## Reproduce baseline and create review packets

From the repository root in PowerShell:

```powershell
uv run --no-sync python metrics/graph_quality.py audit
uv run --no-sync python metrics/graph_quality.py prepare
uv run --no-sync python metrics/build_strict_candidate.py
```

The strict candidate command writes a new versioned export under `data/normalized/`, never overwriting its source.
It applies the schema entity-type and predicate endpoint constraints, records excluded rows under `audit/`, and
reports any remaining target gap. Candidate precision remains null until independent labels are completed.

The audit scans every article, entity row, claim, and relation in the export. It checks evidence/offset integrity,
duplicate triples, graph endpoint types, and endpoint constraints for predicates defined in the code schema. Review
status counts are reported as provenance only, not treated as gold labels. The report is saved to
`metrics/results/v15-global-business-only-full-audit.json` and `.md`.

The prepare command creates a 400-edge simple random sample and a 300-node simple random sample using seed `20261122`, plus
independent double-review packets for 20% of each sample. The packets contain evidence, nearby context, source URL,
language, and candidate labels, but omit extraction rule/model and prior review status to reduce anchoring. Do not use
these packets to tune extraction rules.

Assign the primary edge/node packet to reviewer 1 and the matching `*-double-review.jsonl` packet to reviewer 2.
Reviewers must not see each other's labels. After filling the packets, measure agreement and adjudicate disagreements.
For each row set:

- `verdict`: `correct`, `incorrect`, or `uncertain`;
- `reviewer`: the real reviewer identifier;
- `complete`: `true` only after reviewing all fields and source evidence;
- `review_note`: brief reason for incorrect/uncertain labels.

For edges, `correct` means the evidence supports this exact directed triple, its predicate and temporal/assertion
status, and the relation is in scope. For nodes, it means the entity name, type, identity, and domain inclusion are
correct. Treat unresolved/uncertain cases as incorrect in the conservative precision score unless adjudicated.

## Score completed labels

```powershell
uv run --no-sync python metrics/graph_quality.py score `
  metrics/samples/v15-global-business-only/edges-review.jsonl `
  --kind edges --out metrics/results/v15-global-business-only-edges.json

uv run --no-sync python metrics/graph_quality.py score `
  metrics/samples/v15-global-business-only/nodes-review.jsonl `
  --kind nodes --out metrics/results/v15-global-business-only-nodes.json

uv run --no-sync python metrics/graph_quality.py agreement `
  metrics/samples/v15-global-business-only/edges-review.jsonl `
  metrics/samples/v15-global-business-only/edges-double-review.jsonl `
  --out metrics/results/v15-global-business-only-edge-agreement.json

uv run --no-sync python metrics/graph_quality.py agreement `
  metrics/samples/v15-global-business-only/nodes-review.jsonl `
  metrics/samples/v15-global-business-only/nodes-double-review.jsonl `
  --out metrics/results/v15-global-business-only-node-agreement.json
```

The score reports point precision and a 95% Wilson interval. Claim the overall target only when the lower interval
bound is at least `0.90`. Predicate/source/language breakdowns are descriptive unless each subgroup has enough
independent examples; 1–2 observed edges cannot establish per-type precision. The interval assumes independent
sampled items, so interpret it cautiously when many sampled edges come from the same article. Recall requires a
separate blind, exhaustive sentence sample that includes sentences with no predicted relation; this edge review alone
does not measure recall.

No human labels are present yet, so precision remains **unmeasured**. Structural checks and the target count in the
export manifest must not be reported as an accuracy score.

## Bounded enrichment checkpoint (2026-11-22)

An isolated, source-policy-bounded collection checkpoint is stored under `data/datasets/international-business-quality-enrichment-20261122/`.
Its normalized checkpoint export passed structural and schema checks, but these checks do not establish semantic
precision. Exact dedup against the strict v2 baseline found 11 new strict triples; two independent AI reviewers
agreed on 8 as provisionally supported, agreed on 2 to quarantine, and disagreed on 1. This is an AI screening result,
not a human gold score. Reconciliation is in `results/quality-enrichment-edge-review-consensus-20261122.jsonl`; the
checkpoint audit and exact-delta report are in `results/quality-enrichment-checkpoint-audit-20261122.json` and
`results/quality-enrichment-checkpoint-20261122.json`. Do not promote the provisional edges to a release export until
human adjudication is complete.

A subsequent bounded TechCrunch/VnExpress checkpoint discovered 400 candidate URLs but processed only the first 20.
It produced one additional strict triple (`Jensen Huang đồng` → Nvidia, `FOUNDED`); the mention contains a relation
fragment and needs entity correction plus human review. It is not precision-qualified. The batch-level audit is
`results/quality-enrichment-round1-batch20-audit-20261122.json`; the exact delta and raw edge are in
`results/quality-enrichment-round1-batch20-20261122.json` and
`results/quality-enrichment-round1-new-strict-edges-20261122.jsonl`. No candidate was published or imported.

## Full-population review packets

To review every source row without sampling, run:

```powershell
uv run --no-sync python metrics/prepare_full_review.py
```

This writes deterministic, hash-pinned packets for all 5,046 relations and 2,817 entity rows under
`metrics/reviews/full-review-20261122/`; the manifest records exact task coverage and shard hashes. Read its README
for the label rubric. Keep submitted AI and human labels in separate directories. Verify coverage and summarize
labels with `metrics/score_full_review.py`; an incomplete review does not produce a population precision score, and
AI labels are reported only as an AI screening share. Use `metrics/summarize_full_review.py` to write the coverage,
group breakdown, and non-correct case ledger as JSON/Markdown/JSONL.

Full-population AI screening is complete for the pinned export: 5,046/5,046 relations and 2,817/2,817 entity rows,
with no missing, duplicate, or incomplete task IDs. Results are in `results/full-review-edges-20261122.md` and
`results/full-review-nodes-20261122.md`; row-level incorrect/uncertain ledgers are in their matching
`*-noncorrect.jsonl` files. AI verdicts marked 4,913 edges correct, 94 incorrect, 39 uncertain; for entities, 2,613
correct, 41 incorrect, and 163 uncertain. This is a complete AI screen of predictions, not an independent human gold
measurement; `precision` remains null until human adjudication. The edge screening does not measure recall. Entity
verdicts assess name/type/identity/domain and should be read separately from the strict graph schema: `PROJECT` and
`ASSET` may be relevant concepts while still outside the currently allowed graph node types.

## Human gold review (300-item budget)

The locked, blind review packet is under `metrics/reviews/human-gold-20261123/`: 150 simple-random edges from 5,046
predicted relations and 150 simple-random connected nodes from 2,664 graph nodes (seed `20261123`, without
replacement). Disconnected entity rows are excluded from the node sample because they are not graph nodes. The Excel
workbook has `Instructions`, `Edges`, and `Nodes` tabs; edit only the four review columns and leave `task_id` intact.
Use `correct`, `incorrect`, or `uncertain`; provide reviewer ID, mark complete, and explain incorrect/uncertain cases.
Count uncertain as incorrect for the conservative estimate unless adjudicated.

After review, import labels and score each population:

```powershell
node metrics/build_human_gold_workbook.mjs # only needed to build a fresh blank workbook
node metrics/import_human_gold_workbook.mjs metrics/reviews/human-gold-20261123/human-gold-review.xlsx metrics/reviews/human-gold-20261123/human-review
uv run --no-sync python metrics/score_human_gold_sample.py --manifest metrics/reviews/human-gold-20261123/manifest.json --labels-dir metrics/reviews/human-gold-20261123/human-review --kind edges --out metrics/results/human-gold-edges.json
uv run --no-sync python metrics/score_human_gold_sample.py --manifest metrics/reviews/human-gold-20261123/manifest.json --labels-dir metrics/reviews/human-gold-20261123/human-review --kind nodes --out metrics/results/human-gold-nodes.json
```

The scorer requires all 150 labels to be complete and reports estimated precision with a 95% Wilson interval. Use
the lower bound for the `>=90%` criterion; with 150 items this requires at least 143 correct and no uncertain or
incorrect labels. These are sample estimates, not exact census scores. Keep this locked sample out of threshold/model
tuning; if tuning is needed, label a separate development set. The interval is an approximation that treats rows as
independent even though edges can cluster by article.
