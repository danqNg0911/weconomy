# AI review summary: global-business-only v15

This is an AI screening pass over the fixed-seed review samples, not independent human gold. Do not report these
scores as verified graph precision.

| Sample | AI verdicts | Conservative point precision | 95% Wilson interval | Numeric gate |
|---|---:|---:|---:|---|
| 400 graph edges | 378 correct, 11 incorrect, 11 uncertain | 94.5% | 91.8%–96.3% | Passes numerically; not a human quality claim |
| 300 connected nodes | 271 correct, 23 incorrect, 6 uncertain | 90.3% | 86.5%–93.2% | Does not pass lower-bound gate |

Uncertain is counted as incorrect. The edge sample clears the chosen numeric gate only under AI-generated labels;
the node sample does not. Both estimates need human review before they can support a quality claim.

## Issues surfaced

- Edge errors repeatedly involved `PROJECT` or country-like targets being treated as company/person/government
  actors, plus uncertain direction, event status, or relation evidence.
- Node errors included project/infrastructure, product, university, and person/organization type or identity mixups.
- A second AI reviewer checked 40 edge tasks disjoint from its primary sample. Raw agreement was 37/40 (92.5%),
  but it labeled every item `correct`, so Cohen's kappa is degenerate and not evidence of strong reviewer reliability.
  Three disagreements need adjudication: `edge-0215`, `edge-0238`, and `edge-0183`.
- A second AI reviewer checked 60 node tasks. Raw agreement was 54/60 (90.0%) and Cohen's kappa was 0.46.
  Disagreements include government-agency type, project-vs-entity scope, and a truncated person name; see the
  machine-readable node-agreement result for each reviewer note.

## Files

- Edge labels and notes: `metrics/reviews/agent-review-20261122/edges-agent-labeled.jsonl`.
- Node labels and notes: `metrics/reviews/agent-review-20261122/nodes-agent-labeled.jsonl`.
- Machine-readable edge score: `metrics/results/v15-ai-review-edges.json`.
- Machine-readable node score: `metrics/results/v15-ai-review-nodes.json`.
- Edge reviewer agreement: `metrics/results/v15-ai-review-edge-agreement.json`.
- Node reviewer agreement: `metrics/results/v15-ai-review-node-agreement.json`.
- Original unlabelled reviewer packets remain under `metrics/samples/v15-global-business-only/`.

Next step: have human reviewers independently inspect the labeled edge/node packets, especially incorrect, uncertain,
and disagreed cases. Keep the held-out test unchanged while correcting extraction rules; run a fresh locked test for a
claim of precision at or above 90%.

