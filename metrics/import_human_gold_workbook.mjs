import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile } from "@oai/artifact-tool";

const input = path.resolve(process.argv[2] ?? "metrics/reviews/human-gold-20261123/human-gold-review.xlsx");
const outputDir = path.resolve(process.argv[3] ?? path.join(path.dirname(input), "human-review"));
const workbook = await SpreadsheetFile.importXlsx(new Uint8Array(await fs.readFile(input)));
await fs.mkdir(outputDir, { recursive: true });

for (const [sheetName, kind, lastCol, mapping] of [
  ["Edges", "edges", "Q", { verdict: 13, reviewer: 14, complete: 15, review_note: 16 }],
  ["Nodes", "nodes", "K", { verdict: 7, reviewer: 8, complete: 9, review_note: 10 }],
]) {
  const sheet = workbook.worksheets.getItem(sheetName);
  const rows = sheet.getRange(`A1:${lastCol}151`).values;
  const labels = rows.slice(1).map((values) => ({
    task_id: String(values[0] ?? ""),
    verdict: String(values[mapping.verdict] ?? "").trim().toLowerCase(),
    reviewer: String(values[mapping.reviewer] ?? "").trim(),
    complete: values[mapping.complete] === true || String(values[mapping.complete]).trim().toLowerCase() === "yes",
    review_note: String(values[mapping.review_note] ?? "").trim(),
  }));
  const out = path.join(outputDir, `${kind}.jsonl`);
  await fs.writeFile(out, labels.map((row) => JSON.stringify(row)).join("\n") + "\n", "utf8");
  console.log(`${kind}: ${labels.length} rows -> ${out}`);
}
