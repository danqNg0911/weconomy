-- Weconomy — exploratory DuckDB SQL for ONE selected final run of Parquet files.
-- Run locally in DuckDB, NOT in Neo4j Browser. Replace PATH_TO_FINAL_RUN.
-- The table names are from the supplied Codex report; property names must be
-- confirmed via DESCRIBE / SELECT * before running optional field-based queries.
-- If a file is inside a batch subdirectory, replace path with an appropriate glob.

-- H01. Create transient views (skip any missing table in your selected run).
CREATE OR REPLACE TEMP VIEW bronze AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/bronze.parquet', union_by_name=true);
CREATE OR REPLACE TEMP VIEW articles AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/articles.parquet', union_by_name=true);
CREATE OR REPLACE TEMP VIEW sentences AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/sentences.parquet', union_by_name=true);
CREATE OR REPLACE TEMP VIEW mentions AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/mentions.parquet', union_by_name=true);
CREATE OR REPLACE TEMP VIEW entities AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/entities.parquet', union_by_name=true);
CREATE OR REPLACE TEMP VIEW relations AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/relations.parquet', union_by_name=true);
CREATE OR REPLACE TEMP VIEW events AS SELECT * FROM read_parquet('PATH_TO_FINAL_RUN/**/events.parquet', union_by_name=true);

-- H02. Inspect schemas (run each independently).
DESCRIBE articles;
DESCRIBE sentences;
DESCRIBE mentions;
DESCRIBE entities;
DESCRIBE relations;
DESCRIBE events;

-- H03. Data samples (one per table)
SELECT * FROM bronze LIMIT 3;
SELECT * FROM articles LIMIT 3;
SELECT * FROM sentences LIMIT 3;
SELECT * FROM mentions LIMIT 3;
SELECT * FROM entities LIMIT 3;
SELECT * FROM relations LIMIT 3;
SELECT * FROM events LIMIT 3;

-- H04. Record counts across tiers (row-count ≠ automatically unique objects)
SELECT 'bronze' AS table_name, count(*) AS rows FROM bronze
UNION ALL SELECT 'articles', count(*) FROM articles
UNION ALL SELECT 'sentences', count(*) FROM sentences
UNION ALL SELECT 'mentions', count(*) FROM mentions
UNION ALL SELECT 'entities', count(*) FROM entities
UNION ALL SELECT 'relations_as_claims', count(*) FROM relations
UNION ALL SELECT 'events', count(*) FROM events;

-- H05. Source distribution (assuming source_id exists in articles)
SELECT source_id, count(*) AS articles FROM articles
GROUP BY source_id ORDER BY articles DESC;

-- H06. Language distribution (assuming language exists in articles)
SELECT language, count(*) AS articles FROM articles
GROUP BY language ORDER BY articles DESC;

-- H07. Source x language
SELECT source_id, language, count(*) AS articles
FROM articles GROUP BY source_id, language ORDER BY articles DESC;

-- H08. Unique articles, if article_id and url fields exist
SELECT count(*) AS rows, count(DISTINCT article_id) AS article_ids,
       count(DISTINCT url) AS unique_urls FROM articles;

-- H09. Missing key fields (adapt columns to observed schema)
SELECT count(*) AS total,
       count(*) FILTER (WHERE article_id IS NULL) AS missing_article_id,
       count(*) FILTER (WHERE source_id IS NULL) AS missing_source_id,
       count(*) FILTER (WHERE title IS NULL OR trim(title)='') AS missing_title
FROM articles;

-- H10. Publication year, for timestamp-like published_at
SELECT year(try_cast(published_at AS TIMESTAMP)) AS pub_year,
       count(*) AS articles
FROM articles GROUP BY pub_year ORDER BY pub_year;

-- H11. Publication month (for reports on collection temporal coverage)
SELECT strftime(try_cast(published_at AS TIMESTAMP),'%Y-%m') AS pub_month,
       count(*) AS articles FROM articles GROUP BY pub_month ORDER BY pub_month;

-- H12. Article text length (replace text with actual column name: body/content/text)
SELECT min(length(text)) AS min_chars,
       round(avg(length(text)),1) AS mean_chars,
       median(length(text)) AS median_chars,
       max(length(text)) AS max_chars
FROM articles;

-- H13. Length bins, after determining text column name
SELECT CASE WHEN length(text)<300 THEN '<300'
            WHEN length(text)<1000 THEN '300-999'
            WHEN length(text)<3000 THEN '1000-2999'
            ELSE '>=3000' END AS chars_bucket,
       count(*) AS articles
FROM articles GROUP BY chars_bucket ORDER BY chars_bucket;

-- H14. Sentence counts by article_id (choose correct ID after DESCRIBE)
SELECT article_id,count(*) AS sentences_per_article
FROM sentences GROUP BY article_id ORDER BY sentences_per_article DESC LIMIT 20;

-- H15. Distinct canonical entities (assuming entity_id)
SELECT count(*) AS entity_rows, count(DISTINCT entity_id) AS unique_entity_ids
FROM entities;

-- H16. Canonical entity type (verify entity_type or type)
SELECT entity_type,count(*) AS entities FROM entities
GROUP BY entity_type ORDER BY entities DESC;

-- H17. Mention count and distinct articles (verify IDs)
SELECT count(*) AS mentions_total,
       count(DISTINCT article_id) AS articles_with_mentions,
       count(DISTINCT entity_id) AS linked_entities
FROM mentions;

-- H18. Top-mentioned entities (if entity_id and surface exist)
SELECT entity_id, count(*) AS mentions,
       min(surface) AS example_surface
FROM mentions GROUP BY entity_id ORDER BY mentions DESC LIMIT 30;

-- H19. Claims by predicate — IMPORTANT: 'relations.parquet' are evidence-backed claims
SELECT predicate, count(*) AS extracted_claims
FROM relations GROUP BY predicate ORDER BY extracted_claims DESC;

-- H20. Number of distinct events supported by relations (verify event_id)
SELECT count(*) AS claim_rows, count(DISTINCT event_id) AS distinct_events
FROM relations;

-- H21. Claims per event (verify event_id)
SELECT event_id, count(*) AS claims_supporting_event
FROM relations WHERE event_id IS NOT NULL
GROUP BY event_id ORDER BY claims_supporting_event DESC LIMIT 30;

-- H22. Missing NLP relation metadata (verify names)
SELECT count(*) AS claims,
       count(*) FILTER (WHERE predicate IS NULL) AS no_predicate,
       count(*) FILTER (WHERE event_id IS NULL) AS no_event_id,
       count(*) FILTER (WHERE evidence IS NULL OR trim(evidence)='') AS no_evidence
FROM relations;

-- H23. Examples for manual assessment (verify subject/object column names)
SELECT predicate, subject_id, object_id, left(evidence,240) AS evidence_excerpt
FROM relations ORDER BY random() LIMIT 30;

-- H24. Suggested per-predicate stratified sample for human annotation
WITH sampled AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY predicate ORDER BY random()) AS sampling_row
  FROM relations WHERE predicate IS NOT NULL
)
SELECT predicate,subject_id,object_id,left(evidence,600) AS evidence_excerpt
FROM sampled WHERE sampling_row <= 10 ORDER BY predicate,sampling_row;

-- H25. Distinct articles vs claimed events by source (requires joining by correct document key)
-- SELECT a.source_id, count(DISTINCT a.article_id) AS articles,
--        count(DISTINCT r.event_id) AS events
-- FROM articles a LEFT JOIN relations r ON r.article_id=a.article_id
-- GROUP BY a.source_id ORDER BY events DESC;

-- H26. If export JSONL exists, count JSONL records independently (Python helper):
-- python -c "from pathlib import Path; p=Path('articles.jsonl'); print(sum(1 for _ in p.open(encoding='utf-8')))"
-- Repeat for claims.jsonl, relations.jsonl, entities.jsonl; do not confuse export relations with claim rows.
