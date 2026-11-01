"""Register manually captured, attributed real-source excerpts (no network requests)."""
import hashlib
import json
from pathlib import Path

from weconomy.pipeline import now

root = Path(__file__).resolve().parents[1] / "samples" / "excerpts"
specs = [
    ("disney-pixar", "https://en.wikinews.org/wiki/Disney_buys_Pixar", "2006-01-24"),
    ("microsoft-medstory", "https://en.wikinews.org/wiki/Microsoft_to_acquire_health_information_search_engine",
     "2007-02-27"),
    ("microsoft-github", "https://en.wikinews.org/wiki/Technology_giant_Microsoft_completes_acquisition_of_GitHub",
     "2018-10-29"),
    ("microsoft-vi", "https://vi.wikipedia.org/wiki/Microsoft", ""),
]
documents = []
for name, url, date in specs:
    vi = name.endswith("-vi")
    documents.append({"path": name + ".html", "url": url,
        "source_id": "wikipedia_vi" if vi else "wikinews_en",
        "kind": "encyclopedia_reference" if vi else "news",
        "license": "CC-BY-SA-4.0" if vi else "CC-BY-2.5",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/" if vi
                       else "https://creativecommons.org/licenses/by/2.5/",
        "published_at": date, "language_hint": "vi" if vi else "en", "retrieved_at": now(),
        "sha256": hashlib.sha256((root / (name + ".html")).read_bytes()).hexdigest(),
        "attribution": f"{'Wikipedia contributors' if vi else 'Wikinews'}; {url}; {url}?action=history",
        "capture_method": "Licensed verbatim excerpt read via search tool on 2026-10-30; local HTML wrapper",
        "notes": "Not a full-page download. Selected paragraphs; citation markers/links removed; "
                 "no images. Content is real-source text, not generated news."})
with (root / "manifest.json").open("x", encoding="utf-8") as stream:
    json.dump({"documents": documents}, stream, ensure_ascii=False, indent=2)
