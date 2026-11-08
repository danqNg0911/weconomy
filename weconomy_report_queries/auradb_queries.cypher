// Weconomy report queries — Neo4j AuraDB / Cypher 5+
// READ ONLY. Execute each Q separately in Neo4j Browser, or use collect_auradb.py.
// Levels: [core] first, [extended] next, [heavy] after reviewing dataset size.
// Assumptions for graph-specific queries: (:Entity), .entity_id, .name,
// .type/.entity_type, .domain_types, edge .event_id/.document_ids/.source_ids.
// Check Q05-Q08 before adapting properties to actual database schema.

// Q01 [core] Database version (may require permissions)
CALL dbms.components() YIELD name, versions, edition
RETURN name, versions, edition;

// Q02 [core] Node labels
CALL db.labels() YIELD label RETURN label ORDER BY label;

// Q03 [core] Relationship types (registered types may have zero instances)
CALL db.relationshipTypes() YIELD relationshipType
RETURN relationshipType ORDER BY relationshipType;

// Q04 [core] Database constraints and indexes (two separate commands: Q04a and Q04b)
// Q04a [core] Constraints
SHOW CONSTRAINTS;

// Q04b [core] Indexes
SHOW INDEXES;

// Q05 [core] Sample nodes + all property keys
MATCH (n) RETURN labels(n) AS labels, properties(n) AS node_properties LIMIT 8;

// Q06 [core] Sample relationships + both endpoints
MATCH (a)-[r]->(b)
RETURN labels(a) AS from_labels, properties(a) AS from_properties,
       type(r) AS predicate, properties(r) AS edge_properties,
       labels(b) AS to_labels, properties(b) AS to_properties LIMIT 8;

// Q07 [extended] Node property coverage (whole graph)
MATCH (n)
UNWIND keys(n) AS property
RETURN property, count(*) AS nodes_with_property ORDER BY nodes_with_property DESC;

// Q08 [extended] Relationship property coverage (whole graph)
MATCH ()-[r]->()
UNWIND keys(r) AS property
RETURN property, count(*) AS edges_with_property ORDER BY edges_with_property DESC;

// Q09 [core] Total nodes
MATCH (n) RETURN count(*) AS nodes_all;

// Q10 [core] Total relationships
MATCH ()-[r]->() RETURN count(*) AS edges_all;

// Q11 [core] Nodes labeled Entity
MATCH (n:Entity) RETURN count(*) AS entity_nodes;

// Q12 [extended] Non-Entity node count
MATCH (n) WHERE NOT n:Entity RETURN count(*) AS other_nodes;

// Q13 [core] Node count by label (multi-label nodes appear multiple times)
MATCH (n) UNWIND labels(n) AS label
RETURN label, count(*) AS nodes ORDER BY nodes DESC;

// Q14 [core] Relationship count by actual predicate
MATCH ()-[r]->()
RETURN type(r) AS predicate, count(*) AS edges ORDER BY edges DESC;

// Q15 [core] Node types; check Q05 for actual type property
MATCH (n:Entity)
RETURN coalesce(n.entity_type, n.type, n.kind, n.category, 'UNKNOWN') AS entity_type,
       count(*) AS nodes ORDER BY nodes DESC;

// Q16 [core] Business/domain labels (assuming domain_types is LIST)
MATCH (n:Entity)
UNWIND coalesce(n.domain_types, []) AS domain_type
RETURN domain_type, count(*) AS nodes ORDER BY nodes DESC;

// Q17 [extended] Nodes missing business/domain classifications
MATCH (n:Entity)
RETURN count(*) AS nodes_all,
       sum(CASE WHEN n.domain_types IS NULL OR size(n.domain_types) = 0 THEN 1 ELSE 0 END) AS nodes_without_domain_types;

// Q18 [core] Counts and comparison with project thresholds
MATCH (n:Entity) WITH count(n) AS node_count
MATCH (:Entity)-[r]->(:Entity) WITH node_count, count(r) AS edge_count
RETURN node_count, edge_count,
       node_count >= 2000 AS meets_2000_nodes,
       edge_count >= 5000 AS meets_5000_edges;

// Q19 [extended] Number of USED relation types (distinct from schema-defined predicates)
MATCH ()-[r]->() RETURN count(DISTINCT type(r)) AS observed_relation_types;

// Q20 [core] Relation by source/target entity type
MATCH (a:Entity)-[r]->(b:Entity)
RETURN type(r) AS predicate,
       coalesce(a.entity_type, a.type, a.kind, 'UNKNOWN') AS subject_type,
       coalesce(b.entity_type, b.type, b.kind, 'UNKNOWN') AS object_type,
       count(*) AS edges ORDER BY edges DESC LIMIT 120;

// Q21 [extended] Edge counts by source/target business domain (first domain only)
MATCH (a:Entity)-[r]->(b:Entity)
RETURN coalesce(head(a.domain_types), 'UNCLASSIFIED') AS source_domain,
       type(r) AS predicate,
       coalesce(head(b.domain_types), 'UNCLASSIFIED') AS target_domain,
       count(*) AS edges ORDER BY edges DESC LIMIT 100;

// Q22 [core] Node IDs missing / blank
MATCH (n:Entity)
RETURN count(*) AS total,
       sum(CASE WHEN n.entity_id IS NULL OR trim(toString(n.entity_id)) = '' THEN 1 ELSE 0 END) AS bad_entity_id,
       sum(CASE WHEN n.name IS NULL OR trim(toString(n.name)) = '' THEN 1 ELSE 0 END) AS missing_name;

// Q23 [core] Relationship self-loops
MATCH (a:Entity)-[r]->(b:Entity)
WHERE elementId(a) = elementId(b)
RETURN type(r) AS predicate, count(*) AS self_loops ORDER BY self_loops DESC;

// Q24 [extended] Duplicate entity IDs
MATCH (n:Entity) WHERE n.entity_id IS NOT NULL
WITH toString(n.entity_id) AS entity_id, count(*) AS occurrences
WHERE occurrences > 1
RETURN entity_id, occurrences ORDER BY occurrences DESC LIMIT 30;

// Q25 [extended] Duplicate name + type (possible aliases or duplicates; NOT proof of bad deduplication)
MATCH (n:Entity)
WITH toLower(trim(coalesce(n.name,n.canonical_name,''))) AS normalized_name,
     coalesce(n.entity_type,n.type,n.kind,'UNKNOWN') AS entity_type,
     count(*) AS occurrences, collect(n.entity_id)[0..8] AS entity_ids
WHERE normalized_name <> '' AND occurrences > 1
RETURN normalized_name, entity_type, occurrences, entity_ids
ORDER BY occurrences DESC LIMIT 40;

// Q26 [core] Number of isolated Entity nodes
MATCH (n:Entity) WHERE NOT (n)--()
RETURN count(*) AS isolated_entity_nodes;

// Q27 [core] Top 25 entities by total (in+out) degree
MATCH (n:Entity)
WITH n, COUNT { (n)-->() } AS out_degree, COUNT { (n)<--() } AS in_degree
RETURN n.entity_id AS entity_id, coalesce(n.name,n.canonical_name,n.entity_id) AS name,
       coalesce(n.entity_type,n.type,n.kind,'UNKNOWN') AS entity_type,
       in_degree, out_degree, (in_degree+out_degree) AS total_degree
ORDER BY total_degree DESC LIMIT 25;

// Q28 [extended] Top 20 by incoming degree
MATCH (n:Entity)
RETURN n.entity_id AS entity_id, coalesce(n.name,n.canonical_name,n.entity_id) AS name,
       COUNT { (n)<--() } AS in_degree ORDER BY in_degree DESC LIMIT 20;

// Q29 [extended] Top 20 by outgoing degree
MATCH (n:Entity)
RETURN n.entity_id AS entity_id, coalesce(n.name,n.canonical_name,n.entity_id) AS name,
       COUNT { (n)-->() } AS out_degree ORDER BY out_degree DESC LIMIT 20;

// Q30 [core] Degree distribution (counted by edges, including multi-edges)
MATCH (n:Entity)
WITH COUNT { (n)-->() } + COUNT { (n)<--() } AS degree
RETURN degree, count(*) AS entities ORDER BY degree ASC;

// Q31 [extended] Summary of degree
MATCH (n:Entity)
WITH COUNT { (n)-->() } + COUNT { (n)<--() } AS degree
RETURN count(*) AS entities, min(degree) AS min_degree,
       round(avg(degree)*100)/100.0 AS avg_degree,
       max(degree) AS max_degree,
       percentileCont(degree, 0.5) AS median_degree,
       percentileCont(degree, 0.9) AS p90_degree,
       percentileCont(degree, 0.99) AS p99_degree;

// Q32 [core] Simple directed density (unique directed pairs / N*(N-1))
// Unlike the edge multigraph density, this is <=1 if self-loops are excluded.
MATCH (n:Entity) WITH count(n) AS N
MATCH (a:Entity)-[]->(b:Entity)
WHERE a <> b
WITH N, count(DISTINCT [elementId(a),elementId(b)]) AS unique_directed_pairs
RETURN N, unique_directed_pairs,
       CASE WHEN N>1 THEN 1.0*unique_directed_pairs/(N*(N-1)) ELSE null END AS simple_directed_density;

// Q33 [extended] Unique undirected pairs; useful when comparing NetworkX simple graph
MATCH (a:Entity)-[]-(b:Entity)
WHERE elementId(a) < elementId(b)
RETURN count(DISTINCT [elementId(a),elementId(b)]) AS unique_undirected_pairs;

// Q34 [extended] Repeated same predicate between same ordered pair
// May represent separate events; inspect event_id before labeling as duplicate.
MATCH (a:Entity)-[r]->(b:Entity)
WITH elementId(a) AS a_id, elementId(b) AS b_id, type(r) AS predicate,
     count(*) AS edges, count(DISTINCT r.event_id) AS distinct_event_ids
WHERE edges > 1
RETURN a_id, b_id, predicate, edges, distinct_event_ids
ORDER BY edges DESC LIMIT 50;

// Q35 [extended] Entity pairs with multiple distinct predicates
MATCH (a:Entity)-[r]->(b:Entity)
WITH elementId(a) AS a_id, elementId(b) AS b_id,
     collect(DISTINCT type(r)) AS predicates, count(*) AS edges
WHERE size(predicates) > 1
RETURN a_id,b_id,predicates,edges ORDER BY edges DESC LIMIT 30;

// Q36 [extended] Bidirectional entity pairs (sample only)
MATCH (a:Entity)-[r]->(b:Entity)
WHERE elementId(a) < elementId(b) AND EXISTS { MATCH (b)-->(a) }
RETURN DISTINCT coalesce(a.name,a.entity_id) AS a,
       coalesce(b.name,b.entity_id) AS b LIMIT 30;

// Q37 [core] Coverage of provenance fields on relationships
MATCH ()-[r]->()
RETURN count(*) AS total_edges,
       sum(CASE WHEN r.event_id IS NULL THEN 1 ELSE 0 END) AS missing_event_id,
       sum(CASE WHEN r.document_ids IS NULL OR size(r.document_ids) = 0 THEN 1 ELSE 0 END) AS missing_document_ids,
       sum(CASE WHEN r.source_ids IS NULL OR size(r.source_ids) = 0 THEN 1 ELSE 0 END) AS missing_source_ids;

// Q38 [extended] Number of unique event IDs
MATCH ()-[r]->() WHERE r.event_id IS NOT NULL
RETURN count(DISTINCT r.event_id) AS unique_event_ids,
       count(*) AS edges_with_event_id;

// Q39 [extended] Number of supporting documents per relationship (list property)
MATCH ()-[r]->() WHERE r.document_ids IS NOT NULL
RETURN size(r.document_ids) AS document_count, count(*) AS edges
ORDER BY document_count;

// Q40 [core] Source occurrences supporting graph edges
MATCH ()-[r]->()
UNWIND coalesce(r.source_ids,[]) AS source_id
RETURN source_id, count(*) AS supported_edge_occurrences
ORDER BY supported_edge_occurrences DESC LIMIT 50;

// Q41 [extended] Relation count by review state (confirm property name from Q06/Q08)
MATCH ()-[r]->()
RETURN coalesce(r.review_status,r.review_state,r.validation_status,'NOT_RECORDED') AS review_status,
       count(*) AS edges ORDER BY edges DESC;

// Q42 [extended] Relation count by assertion/polarity (confirm property name)
MATCH ()-[r]->()
RETURN coalesce(toString(r.polarity),toString(r.assertion_status),toString(r.negated),'NOT_RECORDED') AS polarity,
       count(*) AS edges ORDER BY edges DESC;

// Q43 [extended] Relation count by event year (only ISO-like dates)
MATCH ()-[r]->() WHERE r.event_date IS NOT NULL
WITH substring(toString(r.event_date),0,4) AS event_year
RETURN event_year,count(*) AS edges ORDER BY event_year;

// Q44 [extended] How many edges share an event_id
MATCH ()-[r]->() WHERE r.event_id IS NOT NULL
WITH r.event_id AS event_id, count(*) AS edges_per_event
RETURN edges_per_event, count(*) AS events ORDER BY edges_per_event;

// Q45 [core] A few examples for each observed predicate (LIMIT 4 per predicate)
// Collect is suitable for a few thousand edges, not very large graph sizes.
MATCH (a:Entity)-[r]->(b:Entity)
WITH type(r) AS predicate,
     {subject:coalesce(a.name,a.entity_id), object:coalesce(b.name,b.entity_id),
      event_id:r.event_id, source_ids:r.source_ids,
      document_ids:r.document_ids} AS example
WITH predicate, collect(example)[0..4] AS examples
RETURN predicate, examples ORDER BY predicate;

// Q46 [core] Top recurring directed pairs (regardless of relation type)
MATCH (a:Entity)-[r]->(b:Entity)
WITH a,b,count(*) AS edges,collect(DISTINCT type(r)) AS predicates
RETURN coalesce(a.name,a.entity_id) AS subject,
       coalesce(b.name,b.entity_id) AS object,
       edges,predicates ORDER BY edges DESC LIMIT 25;

// Q47 [extended] Share of nodes connected to at least 1 other node
MATCH (n:Entity)
WITH COUNT { (n)--() } AS degree
WITH count(*) AS N, sum(CASE WHEN degree > 0 THEN 1 ELSE 0 END) AS active
RETURN N, active, N-active AS isolated,
       CASE WHEN N>0 THEN round(10000.0*active/N)/100.0 ELSE null END AS active_pct;

// Q48 [extended] Top entity type among isolated nodes
MATCH (n:Entity) WHERE NOT (n)--()
RETURN coalesce(n.entity_type,n.type,n.kind,'UNKNOWN') AS entity_type,
       count(*) AS isolated_nodes ORDER BY isolated_nodes DESC;

// Q49 [extended] Edges involving non-Entity nodes
MATCH (a)-[r]->(b)
WHERE NOT a:Entity OR NOT b:Entity
RETURN type(r) AS predicate, count(*) AS edges ORDER BY edges DESC;

// Q50 [extended] Unclassified entities frequently linked (review target for domain_filter)
MATCH (n:Entity)
WHERE n.domain_types IS NULL OR size(n.domain_types)=0
WITH n, COUNT { (n)-->() } + COUNT { (n)<--() } AS degree
RETURN n.entity_id AS entity_id,coalesce(n.name,n.entity_id) AS name,degree
ORDER BY degree DESC LIMIT 30;

// Q51 [extended] Metadata completeness by entity type
MATCH (n:Entity)
RETURN coalesce(n.entity_type,n.type,n.kind,'UNKNOWN') AS entity_type,
       count(*) AS total,
       sum(CASE WHEN n.name IS NOT NULL THEN 1 ELSE 0 END) AS named,
       sum(CASE WHEN n.entity_id IS NOT NULL THEN 1 ELSE 0 END) AS has_id,
       sum(CASE WHEN n.domain_types IS NOT NULL AND size(n.domain_types)>0 THEN 1 ELSE 0 END) AS has_business_domain
ORDER BY total DESC;

// Q52 [extended] Relationship property name presence rates by predicate
MATCH ()-[r]->()
RETURN type(r) AS predicate, count(*) AS total,
       sum(CASE WHEN r.event_id IS NOT NULL THEN 1 ELSE 0 END) AS with_event,
       sum(CASE WHEN r.document_ids IS NOT NULL AND size(r.document_ids)>0 THEN 1 ELSE 0 END) AS with_docs,
       sum(CASE WHEN r.source_ids IS NOT NULL AND size(r.source_ids)>0 THEN 1 ELSE 0 END) AS with_sources
ORDER BY total DESC;

// Q53 [extended] How often each predicate is associated with more than one source
MATCH ()-[r]->()
RETURN type(r) AS predicate,
       sum(CASE WHEN r.source_ids IS NOT NULL AND size(r.source_ids)>1 THEN 1 ELSE 0 END) AS multi_source_edges,
       count(*) AS total_edges ORDER BY multi_source_edges DESC;

// Q54 [extended] Examples with evidence provenance (fields may vary; inspect Q06)
MATCH (a:Entity)-[r]->(b:Entity)
WHERE r.document_ids IS NOT NULL AND size(r.document_ids)>0
RETURN coalesce(a.name,a.entity_id) AS subject,type(r) AS predicate,
       coalesce(b.name,b.entity_id) AS object,
       r.event_id AS event_id,r.document_ids AS document_ids,
       r.source_ids AS source_ids, r.review_status AS review_status
LIMIT 20;

// Q55 [extended] Does Aura expose GDS procedures? (do not assume plugin exists)
SHOW PROCEDURES YIELD name
WHERE name STARTS WITH 'gds.'
RETURN name ORDER BY name LIMIT 30;

// Q56 [extended] Total nodes/edges within Entity subgraph only
MATCH (n:Entity) WITH count(n) AS N
MATCH (a:Entity)-[r]->(b:Entity)
RETURN N AS entity_nodes, count(r) AS internal_entity_edges;

// Q57 [extended] Pair endpoints connected through same event_id: possible repeated event records
MATCH (a:Entity)-[r]->(b:Entity)
WHERE r.event_id IS NOT NULL
WITH elementId(a) AS a_id,elementId(b) AS b_id,type(r) AS predicate,
     r.event_id AS event_id,count(*) AS rows
WHERE rows>1
RETURN a_id,b_id,predicate,event_id,rows ORDER BY rows DESC LIMIT 30;

// Q58 [extended] Relation type fraction
MATCH ()-[r]->()
WITH type(r) AS predicate, count(*) AS edges
WITH collect({predicate:predicate, edges:edges}) AS items, sum(edges) AS total
UNWIND items AS row
RETURN row.predicate AS predicate, row.edges AS edges,
       CASE WHEN total>0 THEN round(10000.0*row.edges/total)/100.0 ELSE 0 END AS pct
ORDER BY edges DESC;

// Q59 [extended] One query to visualize a small neighborhood: REPLACE entity ID
MATCH (n:Entity {entity_id:'REPLACE_WITH_ENTITY_ID'})-[r]-(m)
RETURN n,r,m LIMIT 50;

// Q60 [heavy] Shortest paths only for a user-selected pair; REPLACE IDs. Use LIMIT.
// MATCH p = shortestPath((a:Entity {entity_id:'REPLACE_A'})-[*..8]-(b:Entity {entity_id:'REPLACE_B'}))
// RETURN p LIMIT 1;
