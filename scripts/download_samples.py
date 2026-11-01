"""Fetch a tiny licensed corpus. Never overwrite an existing snapshot."""
import hashlib
import json
import sys
from pathlib import Path

from weconomy.access import Access
from weconomy.pipeline import load_config, now

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("disney-pixar", "https://en.wikinews.org/wiki/Disney_buys_Pixar", "2006-01-24"),
    ("microsoft-medstory", "https://en.wikinews.org/wiki/Microsoft_to_acquire_health_information_search_engine",
     "2007-02-27"),
    ("microsoft-github", "https://en.wikinews.org/wiki/Technology_giant_Microsoft_completes_acquisition_of_GitHub",
     "2018-10-29"),
    ("microsoft-vi", "https://vi.wikipedia.org/wiki/Microsoft", ""),
]


def main():
    destination = ROOT / "samples" / "manifest.json"
    if destination.exists():
        raise FileExistsError("Sample manifest already exists; keep it for reproducibility")
    destination.parent.mkdir(parents=True, exist_ok=True)
    access = Access(load_config(ROOT / "config/pipeline.yaml"))
    documents, errors = [], []
    try:
        for name, url, date in SOURCES:
            try:
                result = access.fetch(url)
                source = result["source"]
                if "text/html" not in result["headers"].get("content-type", ""):
                    raise ValueError("Expected an HTML page")
                path = destination.parent / f"{name}.html"
                with path.open("xb") as stream:
                    stream.write(result["body"])
                documents.append({"path": path.name, "url": result["url"], "source_id": result["source_id"],
                    "kind": source["kind"], "license": source["license"], "published_at": date,
                    "language_hint": source["language"], "retrieved_at": now(),
                    "sha256": hashlib.sha256(result["body"]).hexdigest(),
                    "attribution": f"Wikimedia contributors; {url}; {url}?action=history; "
                                   f"license policy: {source['terms_url']}",
                    "notes": "Original HTML text snapshot, no linked images downloaded; not a synthetic article"})
            except Exception as exc:
                errors.append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
    finally:
        access.close()
    destination.write_text(json.dumps({"documents": documents, "errors": errors}, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print(json.dumps({"downloaded": len(documents), "errors": errors}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
