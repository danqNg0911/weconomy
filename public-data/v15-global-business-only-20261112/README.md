# AuraDB global business graph snapshot

`entities.jsonl` and `relations.jsonl` are direct exports of the current Neo4j AuraDB graph. The
snapshot includes the stored node and relationship properties, not a graph rebuilt from local
normalized data. AuraDB currently has only `Entity` nodes; claims and articles are not graph nodes.
`claims.jsonl` and `articles.jsonl` remain text-free supporting sidecars from the v15 normalized
release so chatbot clients can resolve claim and document IDs. They are not part of the AuraDB graph.

## Contents

- `entities.jsonl`: 2,664 AuraDB `Entity` nodes with their stored properties.
- `relations.jsonl`: 5,046 AuraDB relationships with their stored properties and endpoints.
- `claims.jsonl`: 5,362 claim records with IDs, predicates, provenance IDs, and review status; no quote text.
- `articles.jsonl`: 923 document records with title, URL, date, language, and content hash; no article body.
- `manifest.json`: AuraDB snapshot time, graph fingerprint, counts, and file hashes.

The claims and articles sidecars have no article body or evidence quote. The full article/evidence bundle
remains access-controlled for group members and is required to build the chatbot's evidence index.

## Import into local Neo4j

From the repository root, set `NEO4J_PASSWORD` in the ignored `.env`, then start Neo4j and import:

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
$env:NEO4J_PASSWORD = ((Get-Content .env | Where-Object { $_ -like 'NEO4J_PASSWORD=*' }) -split '=', 2)[1].Trim().Trim('"').Trim("'")
docker compose up -d neo4j
$env:NEO4J_URI = 'bolt://localhost:7687'
$env:NEO4J_USERNAME = 'neo4j'
$env:NEO4J_DATABASE = 'neo4j'
uv run --no-sync weconomy import-neo4j public-data/v15-global-business-only-20261112
Remove-Item Env:NEO4J_PASSWORD,Env:NEO4J_URI,Env:NEO4J_USERNAME,Env:NEO4J_DATABASE
```

See [Neo4j local setup](../../docs/commands.md#neo4j-local) and [chatbot setup](../../apps/chatbot/README.md).
To run the evidence-grounded chatbot, members need read access to the group's evidence bundle and should
follow the private evidence download steps in the chatbot README. Do not commit `.env`, the evidence cache,
raw HTML, or full article text.

## Refresh from AuraDB and integrity

After the graph is loaded into AuraDB, refresh the node and relationship files directly from AuraDB with:

```powershell
.\scripts\export_public_graph_from_aura.ps1
```

This uses the read-only AuraDB connection in the repository root `.env`; it does not write to AuraDB.
The full evidence package and `.env` must not be committed. Verify the exported file hashes against
`manifest.json` before using the snapshot. The repository MIT license applies to code; this data snapshot
has no separate reuse license. Source URLs and publisher attribution remain in the supporting sidecars.
