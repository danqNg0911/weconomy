import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const base = new URL("./reviews/human-gold-20261123/", import.meta.url).pathname.replace(/^\/(\w:)/, "$1");
const output = `${base}human-gold-review.xlsx`;

async function readJsonl(name) {
  const text = await fs.readFile(`${base}${name}`, "utf8");
  return text.trim().split(/\r?\n/).map((line) => JSON.parse(line));
}

const edges = await readJsonl("edges-review.jsonl");
const nodes = await readJsonl("nodes-review.jsonl");
if (edges.length !== 150 || nodes.length !== 150) throw new Error("Expected 150 tasks per population");

const workbook = Workbook.create();
const instructions = workbook.worksheets.add("Instructions");
instructions.showGridLines = false;
instructions.getRange("A1:B9").values = [
  ["Human gold review", ""],
  ["Purpose", "Blind human review of a reproducible sample from the graph export."],
  ["Sample", "150 edges from 5,046 predicted relations and 150 connected nodes from 2,664 graph nodes."],
  ["Labels", "Choose correct, incorrect, or uncertain. Do not guess when the source does not resolve the case."],
  ["Edge review", "Verify both endpoint identities and types, direction, predicate, assertion or time status, evidence, and domain scope."],
  ["Node review", "Verify the name, type, identity, and business-domain inclusion using the source examples."],
  ["Completion", "Enter reviewer ID, choose a verdict, set complete to Yes, and explain incorrect or uncertain labels."],
  ["Blinding", "No AI verdict, extraction rule, model, or prior review status is shown."],
  ["Scoring", "Keep task_id unchanged. Save the completed workbook and its manifest together for scoring."]
];
instructions.getRange("A1:B1").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 14, bold: true, color: "#FFFFFF" },
};
instructions.getRange("A2:A9").format = { font: { name: "Arial", size: 10, bold: true } };
instructions.getRange("A1:B9").format.verticalAlignment = "center";
instructions.getRange("B2:B9").format.wrapText = true;
instructions.getRange("A:A").format.columnWidth = 20;
instructions.getRange("B:B").format.columnWidth = 100;
instructions.getRange("A1:B9").format.rowHeight = 32;
instructions.getRange("A1:B1").format.rowHeight = 28;

const edgeSheet = workbook.worksheets.add("Edges");
edgeSheet.showGridLines = false;
const edgeHeaders = [
  "task_id", "subject_name", "subject_type", "predicate", "object_name", "object_type",
  "assertion_status", "evidence", "context", "title", "source", "language", "url",
  "verdict", "reviewer", "complete", "review_note",
];
const edgeRows = edges.map((row) => [
  row.task_id, row.subject.name, row.subject.type, row.predicate, row.object.name, row.object.type,
  row.assertion_status, row.evidence, row.context, row.title, row.source, row.language, row.url,
  "", "", "", "",
]);
edgeSheet.getRangeByIndexes(0, 0, 1, edgeHeaders.length).values = [edgeHeaders];
edgeSheet.getRangeByIndexes(1, 0, edgeRows.length, edgeHeaders.length).values = edgeRows;
edgeSheet.getRange("A1:Q1").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  wrapText: true,
  verticalAlignment: "center",
};
edgeSheet.getRange("A2:Q151").format.font = { name: "Arial", size: 10, color: "#1F1F1F" };
edgeSheet.getRange("A2:Q151").format.verticalAlignment = "top";
edgeSheet.getRange("H2:J151").format.wrapText = true;
edgeSheet.getRange("M2:M151").format.wrapText = true;
edgeSheet.getRange("Q2:Q151").format.wrapText = true;
for (const [column, width] of Object.entries({
  A: 14, B: 24, C: 14, D: 24, E: 28, F: 14, G: 18, H: 48, I: 58,
  J: 42, K: 18, L: 12, M: 48, N: 18, O: 20, P: 14, Q: 48,
})) edgeSheet.getRange(`${column}:${column}`).format.columnWidth = width;
edgeSheet.getRange("A2:Q151").format.rowHeight = 118;
edgeSheet.getRange("A1:Q1").format.rowHeight = 32;
edgeSheet.getRange("N2:N151").dataValidation = {
  rule: { type: "list", values: ["correct", "incorrect", "uncertain"] },
};
edgeSheet.getRange("P2:P151").dataValidation = { rule: { type: "list", values: ["Yes", "No"] } };
edgeSheet.freezePanes.freezeRows(1);
edgeSheet.freezePanes.freezeColumns(4);
edgeSheet.tables.add("A1:Q151", true, "EdgeHumanReview");

const nodeSheet = workbook.worksheets.add("Nodes");
nodeSheet.showGridLines = false;
const nodeHeaders = [
  "task_id", "entity_id", "candidate_name", "candidate_type", "connected_in_graph",
  "evidence_count", "evidence_examples", "verdict", "reviewer", "complete", "review_note",
];
const nodeRows = nodes.map((row) => [
  row.task_id, row.entity_id, row.candidate_name, row.candidate_type, row.connected_in_graph,
  row.evidence_count,
  row.evidence_examples.map((example, index) =>
    `Example ${index + 1} (${example.language}, ${example.url})\n` +
    `${example.predicate} / ${example.role} / ${example.other_entity}\n` +
    `Evidence: ${example.evidence}\nContext: ${example.context}`
  ).join("\n\n"),
  "", "", "", "",
]);
nodeSheet.getRangeByIndexes(0, 0, 1, nodeHeaders.length).values = [nodeHeaders];
nodeSheet.getRangeByIndexes(1, 0, nodeRows.length, nodeHeaders.length).values = nodeRows;
nodeSheet.getRange("A1:K1").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  wrapText: true,
  verticalAlignment: "center",
};
nodeSheet.getRange("A2:K151").format.font = { name: "Arial", size: 10, color: "#1F1F1F" };
nodeSheet.getRange("A2:K151").format.verticalAlignment = "top";
nodeSheet.getRange("G2:G151").format.wrapText = true;
nodeSheet.getRange("K2:K151").format.wrapText = true;
for (const [column, width] of Object.entries({
  A: 14, B: 28, C: 36, D: 20, E: 22, F: 16, G: 85, H: 18, I: 20, J: 14, K: 48,
})) nodeSheet.getRange(`${column}:${column}`).format.columnWidth = width;
nodeSheet.getRange("A2:K151").format.rowHeight = 132;
nodeSheet.getRange("A1:K1").format.rowHeight = 32;
nodeSheet.getRange("H2:H151").dataValidation = {
  rule: { type: "list", values: ["correct", "incorrect", "uncertain"] },
};
nodeSheet.getRange("J2:J151").dataValidation = { rule: { type: "list", values: ["Yes", "No"] } };
nodeSheet.freezePanes.freezeRows(1);
nodeSheet.freezePanes.freezeColumns(3);
nodeSheet.tables.add("A1:K151", true, "NodeHumanReview");

workbook.recalculate();
const inspection = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 3500,
  tableMaxRows: 3,
  tableMaxCols: 6,
  tableMaxCellChars: 80,
});
console.log(inspection.ndjson);
const preview = await workbook.render({ sheetName: "Edges", range: "A1:Q5", scale: 1, format: "png" });
await fs.writeFile(`${base}human-gold-review-preview.png`, new Uint8Array(await preview.arrayBuffer()));
const file = await SpreadsheetFile.exportXlsx(workbook);
await file.save(output);
console.log(`saved ${output}; edges=${edgeRows.length}; connected_nodes=${nodeRows.length}`);
