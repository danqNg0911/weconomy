# Global business graph export v15

This is the text-free public projection of the normalized export pinned in `manifest.json`.
It contains graph entities, relations, claim/document IDs, source URLs, and attribution metadata.
Original article text, raw HTML, quoted evidence, local source-run paths, and entity domain-evidence
snippets are omitted. The source export and its AI review are research candidates; independent
human-gold precision has not been measured.

## Contents

- `entities.jsonl`: 2,817 entity rows, including 153 isolates.
- `relations.jsonl`: 5,046 normalized graph relations.
- `claims.jsonl`: 5,362 claim records with IDs, predicates, provenance IDs, and review status; no quote text.
- `articles.jsonl`: 923 document records with title, URL, date, language, and content hash; no article body.
- `manifest.json`: counts, source-input hashes, public-file hashes, and omitted-field list.

The graph has 2,664 connected nodes. Neo4j import loads all 2,817 entity rows, preserving the 153 isolated
entities. The full article/evidence bundle remains access-controlled for group members and is required to
build the chatbot's evidence index. This public projection alone supports graph import and traversal, but
does not supply evidence quotes.

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

## Rebuild and integrity

Regenerate this projection from the pinned local export with:

```powershell
uv run --no-sync python scripts/build_public_graph_export.py
```

Verify file hashes against `manifest.json` before importing. The repository MIT license applies to code;
this dataset projection has no separate reuse license. Source URLs and publisher attribution are retained.
