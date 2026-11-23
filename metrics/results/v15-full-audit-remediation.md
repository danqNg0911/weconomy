# Full audit and remediation: global-business-only v15

## Scope and result

The audit covered every row in the normalized export: 923 articles, 2,817 entity rows, 5,362 claims, and 5,046
direct graph edges. It checked all evidence strings and offsets, triple uniqueness, self-edges, endpoint presence,
relation-to-claim support, schema endpoint types, predicate endpoint constraints, and manifest counts.

Full-population integrity checks passed for duplicate triples, missing endpoints, evidence text/offsets, self-edges,
unevidenced triples, manifest counts, and the two excluded Vietnamese business names. This proves that rows link
consistently to stored evidence; it does **not** prove that each sentence entails the claimed fact.

The graph contract does not pass:

- Entity schema permits `PERSON`, `ORG`, `PLACE`, and `GOV`; the export has 128 rows of other types (`PROJECT` 102,
  `ASSET` 26), including 108 connected nodes.
- 153 edges touch an out-of-schema endpoint. Another 69 edges violate a predicate endpoint constraint in the code;
  62 overlap, leaving **160 unique edges** to quarantine or resolve.
- A strict, read-only projection would retain 2,501 connected nodes, 4,886 edges, and 40 predicates. It clears the
  node/type counts but falls **114 edges short** of the 5,000-edge requirement. The source export was not modified.
- 3,995 edges are marked `manually_verified`; 1,051 are `unreviewed`. These workflow labels are not a held-out
  evaluation set and must not be converted into a precision score.
- `CO_INVESTED_WITH`, `INVESTED_IN`, and `CO_FINANCED_WITH` make up 74.2% of edges. TechCrunch supplies 85.0% of
  relation rows; English accounts for 92.4%. `ANTITRUST_ACTION_AGAINST` occurs twice and `SUPPLIES_TO` 24 times.
  Relation coverage is therefore highly uneven across the assignment themes and sources.

## AI review signal, not full gold measurement

AI reviewers checked a fixed random subset of 400 edges and 300 nodes. Edges received 378 `correct`, 11 `incorrect`,
  and 11 `uncertain` labels (94.5% conservative precision; Wilson 95% interval 91.8–96.3%). Nodes received 271
`correct`, 23 `incorrect`, and 6 `uncertain` labels (90.3%; interval 86.5–93.2%). The node sample does not clear the
lower-bound gate.

The AI double-review checks had 37/40 edge decisions in agreement and 54/60 node decisions in agreement. Edge
Cohen's kappa is degenerate because the second reviewer labeled every edge `correct`; node kappa is 0.46. The
disagreements expose material ambiguity in PROJECT scope, government agency types, and incomplete person names.
These AI labels are not human gold, and the sampled rows have now been exposed to AI reviewers. Do not use them as a
blind held-out test or claim that the full graph has 94.5% precision.

## Recommended remediation

1. **Build a strict graph view, preserving the source export.** Exclude the 160 unique graph-contract violations from
   the release view. Correct a node/edge only when article evidence establishes the intended in-scope actor and
   predicate; otherwise leave it quarantined. This yields the measured projection above (2,501 nodes / 4,886 edges).
2. **Recover the edge-count shortfall with evidence-backed enrichment.** Add at least 114 new, distinct relations that
   pass the same node-type, predicate-direction, domain, and evidence checks. Prioritize antitrust and supply-chain
   reporting because the current export has only 2 explicit antitrust-action edges and 24 `SUPPLIES_TO` edges. Do not
   fill the count by weakening the filters or counting support claims as separate edges.
3. **Use the existing AI findings as a triage list only.** Review the 11 AI-flagged incorrect and 11 uncertain edges,
   the 23 flagged incorrect and 6 uncertain nodes, plus all AI reviewer disagreements. The strict full-population
   violations should be corrected/quarantined first.
4. **Run a new blinded human evaluation after fixes.** Freeze the corrected export, draw a fresh edge sample (the
   current one is no longer blind), double-annotate at least 20%, adjudicate disagreements, and report exact triple
   precision, NER/type precision, recall, F1, per-language/source/predicate counts, and Wilson intervals. At n=400,
   at least 372 correct edge decisions are needed for the Wilson lower bound to reach 90% under this scoring rule.
   Keep rare-predicate results descriptive unless those classes receive their own adequate sample.
5. **Release only after two gates pass:** the graph contract and size targets pass on the same export, and the fresh
   human edge-precision lower bound is at least 90%. Keep the raw, strict-projection, and reviewed versions distinct
   with checksums so the report identifies exactly what was measured.

## Reproduce

```powershell
uv run --no-sync python metrics/graph_quality.py audit
```

Machine-readable full audit: `metrics/results/v15-global-business-only-full-audit.json`.
