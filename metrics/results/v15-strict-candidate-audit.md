# Graph structural audit

Export: `D:\Project\weconomy\data\normalized\international-business-v15-manual-20261112-global-business-only-strict-candidate-20261122-v2`

| Measure | Result |
|---|---:|
| articles | 852 |
| entity_rows | 2,501 |
| connected_nodes | 2,501 |
| relations | 4,886 |
| claims | 5,193 |
| relation_types | 40 |

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
| Projected strict graph | 2,501 nodes, 4,886 edges, 40 types |

### Relation status

| Status | Edges |
|---|---:|
| manually_verified | 3,835 |
| unreviewed | 1,051 |

### Predicate counts

| Predicate | Edges |
|---|---:|
| CO_INVESTED_WITH | 2,165 |
| INVESTED_IN | 1,275 |
| FOUNDED | 359 |
| CO_FINANCED_WITH | 243 |
| CEO_OF | 211 |
| ACQUIRED | 142 |
| PARTNERED_WITH | 127 |
| COOPERATES_WITH | 85 |
| SUBSIDIARY_OF | 33 |
| MEMBER_OF | 31 |
| AGREED_TO_ACQUIRE | 26 |
| SUPPLIES_TO | 23 |
| OWNS_STAKE_IN | 18 |
| CONTRACTED_WITH | 15 |
| BOARD_MEMBER_OF | 14 |
| REGULATES | 13 |
| SPUN_OFF_FROM | 13 |
| EXECUTIVE_OF | 12 |
| JOINT_VENTURE_OF | 11 |
| LENT_TO | 10 |
| MERGED_WITH | 10 |
| COMPETES_WITH | 8 |
| PART_OF | 6 |
| PROVIDES_SERVICE_TO | 6 |
| SUED | 5 |
| OPERATES | 3 |
| PROPOSED_TO_ACQUIRE | 3 |
| ANTITRUST_ACTION_AGAINST | 2 |
| CLOSED_INVESTIGATION_INTO | 2 |
| FINANCED | 2 |
| INVESTIGATES | 2 |
| LICENSED_TECH_FROM | 2 |
| PLANS_TO_LIST_ON | 2 |
| AGREED_TO_MERGE_WITH | 1 |
| APPROVED | 1 |
| AWARDED_CONTRACT_TO | 1 |
| DEVELOPS | 1 |
| LISTED_ON | 1 |
| PLANS_TO_INVEST_IN | 1 |
| SETS_TRADE_TARGET_WITH | 1 |

**Precision: unmeasured.** Structural checks do not establish extraction accuracy.
Review status is not an independent precision measurement.
Entity rows without graph edges are reported separately and excluded from connected-node count.
