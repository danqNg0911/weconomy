// Sprint 2 template only: requires installed compatible GDS. Not executed in Sprint 1.
// Project only Entity nodes; provenance nodes must not change business topology.
// Run CALL gds.version() first. Drop the projection manually only if safe to replace it.
CALL gds.graph.project('weconomy', 'Entity', {
  ACQUIRED: {orientation: 'UNDIRECTED'},
  AGREED_TO_ACQUIRE: {orientation: 'UNDIRECTED'},
  INVESTED_IN: {orientation: 'UNDIRECTED'},
  MERGED_WITH: {orientation: 'UNDIRECTED'},
  SUED: {orientation: 'UNDIRECTED'},
  PARTNERED_WITH: {orientation: 'UNDIRECTED'},
  SUPPLIES_TO: {orientation: 'UNDIRECTED'},
  CEO_OF: {orientation: 'UNDIRECTED'},
  FOUNDED: {orientation: 'UNDIRECTED'},
  SUBSIDIARY_OF: {orientation: 'UNDIRECTED'},
  REGULATES: {orientation: 'UNDIRECTED'}
});
CALL gds.degree.stream('weconomy')
YIELD nodeId, score RETURN gds.util.asNode(nodeId).name AS entity, score ORDER BY score DESC;
CALL gds.pageRank.stream('weconomy')
YIELD nodeId, score RETURN gds.util.asNode(nodeId).name AS entity, score ORDER BY score DESC;
CALL gds.louvain.stream('weconomy')
YIELD nodeId, communityId RETURN gds.util.asNode(nodeId).name AS entity, communityId;
// Compare multiedge aggregation and graph versions with NetworkX before claiming agreement.
