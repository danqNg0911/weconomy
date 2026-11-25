# Social network analysis — Neo4j AuraDB

Generated: 2026-11-25  
Source: live, read-only AuraDB graph snapshot.

## AuraDB versus public v15

- AuraDB has 2,664 Entity nodes and 5,046 relationships. The public graph projection has 2,664 entities; the source normalized export had 2,817 entity rows.
- Aura node IDs equal the public projection and its 2,664 relation endpoint IDs. The projection omits 153 source-export isolates to match AuraDB.
- Relation triples match: **True** (5,046 unique triples); full entity property mismatches: 0.
- Full Aura graph property fingerprint matches the public manifest: **True**.

## Network analysis on AuraDB

- Graph: 2,664 nodes, 4,887 unique undirected pairs, 443 components, 0 isolates.
- Largest component: 1,288 nodes (48.3%); connected-pair coverage: 23.5%.
- Mean shortest path across all reachable node pairs in the full graph: **4.924**; the average over all node pairs is undefined because the graph is disconnected.
- Average shortest path in largest component: **4.938**; clustering: 0.314; transitivity: 0.331.
- Degree-preserving null baseline: mean Cᵣ=0.026 (range 0.024–0.028); mean Lᵣ=3.807 (range 3.791–3.820); 5 connected randomizations with the exact same degree sequence, 34,340 swap attempts each, seeds 20261125–20261129.
- Small-world ratios: C/Cᵣ=11.92, L/Lᵣ=1.297; sigma=9.195. Successful swaps per randomization: 26312, 26289, 26053, 26089, 26065.
- Louvain: 37 communities; modularity Q = 0.714.
- Maximum k-core: k=16, 17 nodes.

## PageRank top 30

| Rank | Entity | Type | PageRank |
|---:|---|---|---:|
| 1 | Generalist | ORG | 0.00496979 |
| 2 | Green SM | ORG | 0.00463746 |
| 3 | Lightspeed Venture Partners | ORG | 0.00406069 |
| 4 | Anthropic | ORG | 0.00354318 |
| 5 | Pronto | ORG | 0.00330719 |
| 6 | Nvidia | ORG | 0.00310102 |
| 7 | ElevenLabs | ORG | 0.00304191 |
| 8 | Andreessen Horowitz | ORG | 0.00297326 |
| 9 | Xcimer | ORG | 0.00292538 |
| 10 | OpenAI | ORG | 0.00290985 |
| 11 | Mariana Minerals | ORG | 0.00290813 |
| 12 | Sumitomo Mitsui Banking Corporation | ORG | 0.00290074 |
| 13 | MIT | ORG | 0.0028544 |
| 14 | Legora | ORG | 0.00280083 |
| 15 | RTX | ORG | 0.00271468 |
| 16 | D-ID | ORG | 0.00269802 |
| 17 | Harvey | ORG | 0.00269055 |
| 18 | CFS | ORG | 0.00260613 |
| 19 | General Catalyst | ORG | 0.00258979 |
| 20 | Xflow | ORG | 0.00251085 |
| 21 | Apptronik | ORG | 0.00229925 |
| 22 | Aeternum Consulting | ORG | 0.00223808 |
| 23 | AGRI SMILE | ORG | 0.00219432 |
| 24 | Accel | ORG | 0.00212801 |
| 25 | Rivian | ORG | 0.00210063 |
| 26 | Oura | ORG | 0.00207864 |
| 27 | Counsel Health | ORG | 0.00207323 |
| 28 | SpaceX | ORG | 0.00203038 |
| 29 | Volkswagen Group | ORG | 0.00198453 |
| 30 | India Deep Tech Alliance | ORG | 0.00193751 |

## Maximum core — top 20 by PageRank

| Entity | Type | k | PageRank |
|---|---|---:|---:|
| Sumitomo Mitsui Banking Corporation | ORG | 16 | 0.00290074 |
| Standard Chartered | ORG | 16 | 0.00148693 |
| Commerzbank | ORG | 16 | 0.00121032 |
| Mashreq Bank | ORG | 16 | 0.00121032 |
| Australia and New Zealand Banking Group | ORG | 16 | 0.00121032 |
| CTBC Bank | ORG | 16 | 0.00121032 |
| Cathay United Bank | ORG | 16 | 0.00121032 |
| HSBC | ORG | 16 | 0.00116372 |
| Maybank Securities | ORG | 16 | 0.00107624 |
| Taipei Fubon Commercial Bank | ORG | 16 | 0.00107624 |
| The Bank of East Asia | ORG | 16 | 0.00107624 |
| Doha Bank | ORG | 16 | 0.00107624 |
| National Bank of Kuwait | ORG | 16 | 0.00107624 |
| Oversea-Chinese Banking Corporation Limited | ORG | 16 | 0.00107624 |
| Arab Bank for Investment and Foreign Trade | ORG | 16 | 0.00107624 |
| First Abu Dhabi Bank | ORG | 16 | 0.00107624 |
| Landesbank Baden-Württemberg | ORG | 16 | 0.00107624 |

## Largest 10 communities

| Community | Nodes | PageRank leaders (up to 5) |
|---:|---:|---|
| 1 | 125 | Anthropic, Legora, General Catalyst, Accel, Perplexity |
| 2 | 123 | Andreessen Horowitz, Harvey, Anduril, ASIO, Sequoia Capital |
| 3 | 92 | Nvidia, ElevenLabs, D-ID, T. Rowe Price, BlackRock |
| 4 | 77 | Glow, Index Ventures, DoorDash, Ramp, Greenoaks |
| 5 | 71 | SpaceX, xAI, Amazon, Astrix Security, Cursor |
| 6 | 66 | Xcimer, MIT, RTX, CFS, Google |
| 7 | 60 | Microsoft, Thrive Capital, Helion, Peak XV Partners, First Round Capital |
| 8 | 58 | Lightspeed Venture Partners, Mistral AI, Bpifrance, B Capital, Basis |
| 9 | 54 | Xflow, Drip Capital, AI-based foreign exchange tool, Easebuzz, ChronicleBio |
| 10 | 50 | OpenAI, celld, LMArena, Rosalind life-sciences AI model, Deno |

## Interpretation

- The degree-preserving sigma (9.195) supports the small-world criterion on the largest component; five connected null graphs were used, so their ranges should be reported and the comparison is not a significance test.
- AuraDB is the analysis source. It contains the same 5,046 relation triples as public v15 and excludes the 153 isolated export entities.
- PageRank, communities, and core are structural measures, not a validation of relation precision.

## Reproduction

```powershell
.\metrics\run_social_network_analysis.ps1
```

The JSON includes a SHA-256 fingerprint of all Aura Entity and relationship properties for snapshot tracking.
