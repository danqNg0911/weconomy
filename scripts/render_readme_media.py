"""Render README illustrations from a catalog JSONL export and captured CLI status."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line]


def svg(body: str, width: int, height: int) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#f5f7fa"/>
<style>text{{font-family:"Segoe UI",Arial,sans-serif;fill:#142536}}.muted{{fill:#607386}}.small{{font-size:14px}}
.label{{font-size:13px;font-weight:700;letter-spacing:.7px}}.node{{fill:white;stroke:#b9c8d5;stroke-width:1.5}}
.edge{{stroke:#147d78;stroke-width:2.5;fill:none}}</style>{body}</svg>"""


def graph_svg(entities: list[dict], relations: list[dict], status: dict, max_edges: int) -> str:
    nodes = {row["entity_id"]: row for row in entities}
    unique = {(r.get("subject_id"), r.get("predicate"), r.get("object_id")): r for r in relations}
    all_rows = list(unique.values())
    if not all_rows:
        raise ValueError("Export contains no relation triples")
    rows = all_rows[:max_edges]
    counts = status.get("counts", {})
    body = [
        '<text x="54" y="55" font-size="27" font-weight="700">Ứng viên quan hệ từ catalog thực tế</text>',
        (f'<text x="54" y="84" class="muted small">Dataset export · {counts.get("articles", 0)} bài · '
         f'{counts.get("nodes", 0)} node có cạnh · {len(all_rows)} cạnh phân biệt · '
         f'{counts.get("relation_types", 0)} loại quan hệ</text>'),
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L9,3 z" fill="#147d78"/></marker></defs>',
    ]
    for i, relation in enumerate(rows):
        y = 118 + i * 76
        source, target = nodes.get(relation.get("subject_id"), {}), nodes.get(relation.get("object_id"), {})
        left = escape(str(source.get("name", relation.get("subject_id", "?"))))
        right = escape(str(target.get("name", relation.get("object_id", "?"))))
        predicate = escape(str(relation.get("predicate", "")))
        body.extend([
            f'<rect class="node" x="54" y="{y}" width="270" height="48" rx="9"/>',
            f'<text x="70" y="{y + 20}" class="muted small">{escape(str(source.get("entity_type", "")))}</text>',
            f'<text x="70" y="{y + 39}" font-size="16" font-weight="600">{left}</text>',
            f'<line class="edge" x1="335" y1="{y + 24}" x2="638" y2="{y + 24}" marker-end="url(#arrow)"/>',
            f'<rect x="420" y="{y + 8}" width="132" height="31" rx="15" fill="#e2f1ef"/>',
            f'<text x="486" y="{y + 28}" text-anchor="middle" class="label">{predicate}</text>',
            f'<rect class="node" x="650" y="{y}" width="320" height="48" rx="9"/>',
            f'<text x="666" y="{y + 20}" class="muted small">{escape(str(target.get("entity_type", "")))}</text>',
            f'<text x="666" y="{y + 39}" font-size="16" font-weight="600">{right}</text>',
        ])
    body.append(f'<text x="54" y="{130 + 76 * len(rows)}" class="muted small">'
                f'Hiển thị {len(rows)}/{len(all_rows)} cạnh; đều là ứng viên unreviewed. Không hiển thị câu bài báo.</text>')
    return svg("\n".join(body), 1024, 196 + 76 * len(rows))


def provenance_svg(entities: list[dict], relations: list[dict], articles: list[dict]) -> str:
    nodes = {row["entity_id"]: row for row in entities}
    article_by_id = {row.get("document_id"): row for row in articles}
    relation = relations[0]
    article = article_by_id.get(relation.get("document_id"), {})
    source = nodes.get(relation.get("subject_id"), {})
    target = nodes.get(relation.get("object_id"), {})
    values = [
        ("CANDIDATE TRIPLE", f'{source.get("name", "?")} → {relation.get("predicate", "?")} → {target.get("name", "?")}'),
        ("REVIEW STATUS", str(relation.get("review_status", "unknown"))),
        ("CLAIM ID", str(relation.get("claim_id", "unknown"))),
        ("SOURCE DOCUMENT", f'{relation.get("source_id", "unknown")} · {article.get("document_id", relation.get("document_id", "unknown"))}'),
        ("SOURCE HOST", urlsplit(str(article.get("canonical_url", ""))).hostname or "unavailable"),
        ("EVIDENCE SPAN", f'offsets [{relation.get("evidence_start", "?")}, {relation.get("evidence_end", "?")}) in article body · text not reproduced'),
    ]
    body = [
        '<text x="56" y="54" font-size="27" font-weight="700">Từ cạnh ứng viên về dấu vết nguồn</text>',
        '<text x="56" y="82" class="muted small">Một relation và source document trong export thực tế · không chép câu bài báo</text>',
    ]
    for i, (label, value) in enumerate(values):
        y = 114 + i * 65
        body.extend([
            f'<rect x="54" y="{y}" width="916" height="52" rx="8" fill="{"#e2f1ef" if i == 0 else "white"}" stroke="#b9c8d5"/>',
            f'<text x="72" y="{y + 21}" class="label">{escape(label)}</text>',
            f'<text x="265" y="{y + 33}" font-size="15">{escape(value)}</text>',
        ])
    body.append('<text x="54" y="525" class="muted small">'
                'Offset xác định vị trí câu evidence trong thân bài nguồn; không tái hiện câu báo trong hình.</text>')
    return svg("\n".join(body), 1024, 560)


def status_svgs(status: dict) -> list[str]:
    counts = status.get("counts", {})
    remaining, targets = status.get("remaining") or {}, status.get("targets") or {}
    lines = [
        ("$ uv run --no-sync weconomy dataset-status <dataset>", "#91e6c7"),
        (f'"attempts_allocated": {status.get("attempts_allocated", 0)},', "#e7edf3"),
        (f'"articles": {counts.get("articles", 0)},  "nodes": {counts.get("nodes", 0)},', "#e7edf3"),
        (f'"relations": {counts.get("relations", 0)},  "relation_types": {counts.get("relation_types", 0)},', "#e7edf3"),
        (f'"targets_met": {str(bool(status.get("targets_met", False))).lower()},  "reason": "{status.get("reason", "unknown")}",', "#f0c674"),
        (f'"remaining": nodes {remaining.get("nodes", 0)}, edges {remaining.get("relations", 0)}, types {remaining.get("relation_types", 0)}', "#a9bfd2"),
        (f'"targets": nodes {targets.get("nodes", 0)}, edges {targets.get("relations", 0)}, types {targets.get("relation_types", 0)}', "#a9bfd2"),
    ]
    result = []
    for last in range(1, len(lines) + 1):
        body = [
            '<rect x="22" y="22" width="956" height="556" rx="16" fill="#101c28"/>',
            '<text x="56" y="67" style="fill:#fff" font-size="23" font-weight="700">Weconomy · CLI status replay</text>',
            '<text x="56" y="94" style="fill:#9bb0c2" font-size="14">Phát lại output CLI thực tế · dataset snapshot · JSON rút gọn</text>',
        ]
        body.extend(f'<text x="58" y="{151 + i * 48}" style="fill:{color}" font-family="Consolas,monospace" font-size="18">{escape(text)}</text>'
                    for i, (text, color) in enumerate(lines[:last]))
        body.append('<text x="58" y="535" style="fill:#9bb0c2" font-size="13">'
                    'Số liệu mô tả snapshot; relation candidates chưa được người duyệt.</text>')
        result.append(svg("\n".join(body), 1000, 600))
    return result


def edge_executable() -> Path:
    paths = (Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
             Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"))
    if not (edge := next((p for p in paths if p.exists()), None)):
        raise RuntimeError("Microsoft Edge is required to render SVG media")
    return edge


def render_png(edge: Path, svg_path: Path, png_path: Path, width: int, height: int) -> None:
    run = subprocess.run([
        str(edge), "--headless", "--disable-gpu", "--hide-scrollbars",
        "--allow-file-access-from-files", f"--window-size={width},{height}",
        f"--screenshot={png_path.resolve()}", svg_path.resolve().as_uri(),
    ], capture_output=True, text=True, timeout=45)
    if run.returncode not in (0, 1) or not png_path.exists() or png_path.stat().st_size < 1000:
        raise RuntimeError(f"Edge could not render {svg_path.name}: {run.stderr[-1000:]}")


def make_gif(pngs: list[Path], destination: Path) -> dict:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Install the temporary renderer with: uv run --no-project --with pillow python scripts/render_readme_media.py ...") from exc
    originals = [Image.open(path).convert("RGB") for path in pngs]
    sample = Image.new("RGB", (200, 120 * len(originals)), "#f5f7fa")
    for i, frame in enumerate(originals):
        sample.paste(frame.resize((200, 120), Image.Resampling.LANCZOS), (0, 120 * i))
    palette = sample.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for frame in originals]
    delays = [700] * (len(frames) - 1) + [2500]
    frames[0].save(destination, format="GIF", save_all=True, append_images=frames[1:],
                    duration=delays, loop=0, disposal=2, optimize=False)
    for frame in originals + frames + [sample, palette]:
        frame.close()
    with Image.open(destination) as check:
        count, loop = check.n_frames, check.info.get("loop")
        actual_delays = []
        for i in range(count):
            check.seek(i)
            actual_delays.append(check.info.get("duration"))
    if count != len(pngs) or loop != 0 or actual_delays != delays:
        raise ValueError(f"GIF validation failed: frames={count}, loop={loop}, durations={actual_delays}")
    return {"gif_frames": count, "frame_delays_ms": actual_delays, "loop_forever": True,
            "bytes": destination.stat().st_size}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-dir", type=Path, required=True, help="Directory from export-dataset")
    parser.add_argument("--status-json", type=Path, required=True, help="Captured dataset-status JSON")
    parser.add_argument("--output-dir", type=Path, default=Path("docs/assets"))
    parser.add_argument("--max-edges", type=int, default=8, help="Maximum real relation triples drawn in the preview")
    args = parser.parse_args()
    if args.max_edges < 1:
        parser.error("--max-edges must be positive")
    entities = jsonl(args.export_dir / "entities.jsonl")
    relations = jsonl(args.export_dir / "relations.jsonl")
    claims = jsonl(args.export_dir / "claims.jsonl")
    articles = jsonl(args.export_dir / "articles.jsonl")
    status = json.loads(args.status_json.read_text(encoding="utf-8-sig"))
    unique = {(r.get("subject_id"), r.get("predicate"), r.get("object_id")) for r in relations}
    connected = {entity_id for relation in relations for entity_id in (relation.get("subject_id"), relation.get("object_id"))}
    actual = {"articles": len(articles), "nodes": len(connected), "relations": len(unique), "claims": len(claims),
              "relation_types": len({r.get("predicate") for r in relations})}
    expected = {key: status.get("counts", {}).get(key) for key in actual}
    if actual != expected:
        raise ValueError(f"Status and export counts differ: status={expected}, export={actual}")
    edge = edge_executable()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    svg_files = [
        ("relation-candidates", graph_svg(entities, relations, status, args.max_edges), 1024,
         196 + 76 * min(args.max_edges, len(unique))),
        ("provenance-trace", provenance_svg(entities, relations, articles), 1024, 560),
    ]
    pngs = []
    for name, content, width, height in svg_files:
        source, image = args.output_dir / f"{name}.svg", args.output_dir / f"{name}.png"
        source.write_text(content, encoding="utf-8")
        render_png(edge, source, image, width, height)
        pngs.append(image)
    with tempfile.TemporaryDirectory(prefix="weconomy-readme-") as tmp:
        frames = []
        for i, content in enumerate(status_svgs(status)):
            source, image = Path(tmp) / f"status-{i}.svg", Path(tmp) / f"status-{i}.png"
            source.write_text(content, encoding="utf-8")
            render_png(edge, source, image, 1000, 600)
            frames.append(image)
        gif_info = make_gif(frames, args.output_dir / "dataset-status-replay.gif")
    print(json.dumps({"pngs": [str(p) for p in pngs],
                      "gif": str(args.output_dir / "dataset-status-replay.gif"), **gif_info},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

