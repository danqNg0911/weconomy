# Graph structural audit

Export: `D:\Project\weconomy\data\normalized\international-business-quality-enrichment-20261122-round1-batch20-domain-20261122T140722-57c333`

| Measure | Result |
|---|---:|
| articles | 561 |
| entity_rows | 1,126 |
| connected_nodes | 1,126 |
| relations | 911 |
| claims | 1,049 |
| relation_types | 16 |

Structural checks passed: **True**

| Check | Result |
|---|---:|
| duplicate_article_ids | 0 |
| duplicate_entity_ids | 0 |
| duplicate_relation_claim_ids | 0 |
| duplicate_claim_ids | 0 |
| duplicate_triples | 0 |
| missing_endpoints | 0 |
| missing_claim_endpoints | 0 |
| bad_or_missing_evidence | 0 |
| bad_evidence_offsets | 0 |
| bad_or_missing_claim_evidence | 0 |
| bad_claim_evidence_offsets | 0 |
| self_edges | 0 |
| unevidenced_triples | 0 |
| unconnected_entities | 0 |
| vinpearl_entity_matches | 0 |
| vietnam_airlines_entity_matches | 0 |
| manifest_counts_match | True |

Graph schema checks passed: **True**

## Full-export profile

| Measure | Count |
|---|---:|
| Entity rows outside schema types | 0 |
| Connected nodes outside schema types | 0 |
| Edges with an out-of-schema endpoint | 0 |
| Mapped predicate endpoint type violations | 0 |
| Unique edges to quarantine/review | 0 |
| Projected strict graph | 1,126 nodes, 911 edges, 16 types |

### Relation status

| Status | Edges |
|---|---:|
| unreviewed | 911 |

### Predicate counts

| Predicate | Edges |
|---|---:|
| INVESTED_IN | 383 |
| FOUNDED | 246 |
| CEO_OF | 145 |
| ACQUIRED | 74 |
| PARTNERED_WITH | 27 |
| MERGED_WITH | 7 |
| AGREED_TO_ACQUIRE | 6 |
| SPUN_OFF_FROM | 6 |
| SUBSIDIARY_OF | 6 |
| BOARD_MEMBER_OF | 2 |
| CLOSED_INVESTIGATION_INTO | 2 |
| INVESTIGATES | 2 |
| SUED | 2 |
| LICENSED_TECH_FROM | 1 |
| OWNS_STAKE_IN | 1 |
| SUPPLIES_TO | 1 |

**Precision: unmeasured.** Structural checks do not establish extraction accuracy.
Review status is not an independent precision measurement.
Entity rows without graph edges are reported separately and excluded from connected-node count.
