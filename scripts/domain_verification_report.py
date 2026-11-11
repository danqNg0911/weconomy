"""Inspect a normalized snapshot and prepare a reproducible independent-review sample."""
import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text("utf-8").splitlines() if line]


def inspect(path):
    tables = {kind: jsonl(path / f"{kind}.jsonl") for kind in ("articles", "entities", "relations", "claims")}
    entities = {row["entity_id"] for row in tables["entities"]}
    articles = {row["document_id"]: row for row in tables["articles"]}
    triples = [(row["subject_id"], row["predicate"], row["object_id"]) for row in tables["relations"]]
    connected = {value for subject, _, object_ in triples for value in (subject, object_)}
    claim_triples = {(row["subject_id"], row["predicate"], row["object_id"]) for row in tables["claims"]}
    missing = sum(row["subject_id"] not in entities or row["object_id"] not in entities for row in tables["claims"])
    bad_evidence = sum(row["document_id"] not in articles or row["evidence"] not in
                       articles.get(row["document_id"], {}).get("text", "") for row in tables["claims"])
    bad_offsets = sum(isinstance(row.get("evidence_start"), int) and isinstance(row.get("evidence_end"), int)
                      and articles.get(row["document_id"], {}).get("text", "")[
                          row["evidence_start"]:row["evidence_end"]] != row["evidence"] for row in tables["claims"])
    return {"articles": len(articles), "entities": len(entities), "connected_nodes": len(connected),
            "relations": len(triples), "claims": len(tables["claims"]),
            "relation_types": len({row[1] for row in triples}),
            "duplicate_triples": len(triples) - len(set(triples)), "missing_endpoints": missing,
            "bad_evidence": bad_evidence, "self_edges": sum(a == b for a, _, b in triples),
            "bad_offsets": bad_offsets, "unevidenced_triples": len(set(triples) - claim_triples),
            "duplicate_entity_ids": len(tables["entities"]) - len(entities),
            "duplicate_claim_ids": len(tables["claims"]) - len({row["claim_id"] for row in tables["claims"]}),
            "unconnected_entities": len(entities - connected),
            "by_predicate": dict(Counter(row[1] for row in triples))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("normalized", type=Path)
    parser.add_argument("--baseline", type=Path,
                        default=Path("data/exports/international-business-gliner-v2-domain-v14-dedup-20261108"))
    parser.add_argument("--output", type=Path, default=Path("reports/domain-v15-verification-20261109"))
    args = parser.parse_args()
    manifest = json.loads((args.normalized / "manifest.json").read_text("utf-8"))
    current, baseline = inspect(args.normalized), inspect(args.baseline)
    assert not any(current[key] for key in
                   ("duplicate_triples", "missing_endpoints", "bad_evidence", "self_edges", "unconnected_entities",
                    "bad_offsets", "unevidenced_triples", "duplicate_entity_ids", "duplicate_claim_ids"))
    assert current["connected_nodes"] == manifest["counts"]["nodes"]
    assert current["relations"] == manifest["counts"]["relations"]
    lineage = manifest["lineage"]
    for kind, checksum in lineage["input_sha256"].items():
        assert hashlib.sha256((Path(lineage["source_export"]) / f"{kind}.jsonl").read_bytes()).hexdigest() == checksum
    code = Path(__file__).resolve().parents[1] / "src/weconomy"
    for name, checksum in lineage.get("implementation_sha256", {}).items():
        assert hashlib.sha256((code / name).read_bytes()).hexdigest() == checksum
    audit = jsonl(args.normalized / "audit/claims.jsonl")
    source_articles = {row["document_id"]: row for row in jsonl(Path(lineage["source_export"]) / "articles.jsonl")}
    # Sampling across decision and predicate exposes both retained errors and rejected valid facts.
    groups = defaultdict(list)
    for row in audit:
        article = source_articles.get(row["document_id"], {})
        groups[(row["decision"], row["predicate"], article.get("language", "unknown"),
                urlsplit(article.get("canonical_url", "")).hostname or "unknown",
                row.get("recovery_method", "extracted"))].append(row)
    rng = random.Random(20261109)
    sample = []
    for key in sorted(groups):
        rng.shuffle(groups[key])
        sample.extend(groups[key][:3])
    sample = [{**row, "human_correct_entity_types": None, "human_correct_relation": None,
               "human_in_domain": None, "reviewer": "", "review_note": ""} for row in sample]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    review = args.output.with_suffix(".review.jsonl")
    review.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in sample), encoding="utf-8")
    report = {"normalized": str(args.normalized.resolve()), "baseline": baseline, "current": current,
              "targets": manifest["status"]["targets"], "remaining": manifest["status"]["remaining"],
              "targets_met": manifest["status"]["targets_met"], "filter": manifest["domain_filter"],
              "structural_checks_passed": True, "precision": None,
              "precision_note": "Requires independent labels; filtering and structural checks are not accuracy measurement",
              "review_sample": str(review), "review_sample_size": len(sample), "lineage": lineage}
    args.output.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Kết quả kiểm định domain", "", f"Snapshot: `{args.normalized}`", "",
             f"Baseline: `{args.baseline}`", "",
             "| Chỉ số | Bản trước | Bản hiện tại |", "|---|---:|---:|"]
    for label, key in [("Bài trong export", "articles"), ("Entity xuất", "entities"),
                       ("Nút thực sự có cạnh", "connected_nodes"), ("Triple", "relations"),
                       ("Claim", "claims"), ("Loại quan hệ", "relation_types")]:
        lines.append(f"| {label} | {baseline[key]:,} | {current[key]:,} |")
    lines += ["", f"Đạt chỉ tiêu: **{report['targets_met']}**. Còn thiếu: `{report['remaining']}`.", "",
              "Kiểm tra cấu trúc đã qua: không triple trùng, không self-edge, không đầu mút thiếu,",
              "không entity cô lập trong mạng xuất, câu bằng chứng có trong bài và checksum đầu vào khớp.", "",
              "## Quyết định kiểm định", "", "| Lý do claim | Số lượng |", "|---|---:|"]
    for reason, count in sorted(manifest["domain_filter"]["claim_reasons"].items(), key=lambda x: -x[1]):
        lines.append(f"| {reason} | {count:,} |")
    lines += ["", "## Giới hạn và bước tiếp theo", "",
              "Đây là bộ lọc dựa trên bằng chứng và các cấu trúc ngôn ngữ có hỗ trợ. Nó có thể đưa",
              "quan hệ đúng nhưng diễn đạt khác sang review; số bản ghi bị review không phải số lỗi đã chứng minh.",
              "Chưa có nhãn độc lập để kết luận precision trên 90% hoặc đo recall.", "",
              f"Mẫu phân tầng để gán nhãn: `{review}` ({len(sample)} claim, gồm cả accepted và review).",
              "Không dùng cùng mẫu để vừa chỉnh rule vừa công bố kết quả đánh giá cuối.", "",
              "Tiếp tục bổ sung URL mới bằng graph-cycle theo docs/DOMAIN_VERIFICATION.md.",
              "Bản chưa đủ chỉ tiêu là candidate; chưa dùng để thay bản đang phục vụ hoặc xuất bản."]
    args.output.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(args.output.with_suffix('.md')), "counts": current,
                      "targets_met": report["targets_met"], "review_sample": str(review)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
