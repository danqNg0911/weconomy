# Full-population review

These packets cover every row in the pinned export; they are not random samples. The source export remains unchanged.
`manifest.json` records source hashes, population counts, and each packet shard hash.

## Populations

- 5,046 relation rows, split into 51 edge shards of at most 100 tasks.
- 2,817 entity rows, split into 29 node shards of at most 100 tasks. This includes 2,664 graph-connected nodes and 153 entities not connected by a relation.

The packet generator omits `review_status`, extraction rule/model, and source-run provenance to reduce anchoring.
Each edge task includes the candidate triple, assertion status, evidence, nearby article context, URL, source, and language.
Each node task includes the candidate name/type and up to five distinct evidence examples; mark it `uncertain` if those
examples do not establish identity, type, and domain scope.

## Label rubric

- `correct`: every required field is supported: entity identity/type, directed predicate, assertion/temporal status,
  evidence, and domain inclusion.
- `incorrect`: at least one field is clearly wrong.
- `uncertain`: the provided source context cannot resolve the candidate. Do not guess.

For incorrect/uncertain labels, add a short `review_note` naming the failed or unresolved dimension. Set `complete=true`
only after reading the evidence and context. Reviewers must not see each other's labels before submitting.

## Interpretation

AI verdicts are full-coverage AI screening, not human gold. A full human review gives an exact descriptive score for
this pinned export once every row is complete and disagreements are adjudicated; it does not need a sampling interval.
Do not overwrite the original packets or source export. Save completed labels in separate `ai-review/` or
`human-review/` directories and preserve the manifest for coverage verification.
