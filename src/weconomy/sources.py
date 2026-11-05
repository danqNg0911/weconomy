"""Source inventory and a limited robots/policy probe."""
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .access import Access


def source_status(config, *, check=False, source_ids=None):
    sources = yaml.safe_load(Path(config["sources"]).read_text(encoding="utf-8"))["sources"]
    selected = list(source_ids) if source_ids is not None else list(sources)
    unknown = set(selected) - sources.keys()
    if unknown:
        raise KeyError(f"Unknown source id(s): {', '.join(sorted(unknown))}")

    rows = []
    for source_id in selected:
        source = sources[source_id]
        rows.append({"source_id": source_id, "enabled": bool(source.get("allowed", False)),
                     "kind": source.get("kind"), "language": source.get("language"),
                     "terms_url": source.get("terms_url"),
                     "excluded": source_id in {"wikinews_en", "techcrunch", "reuters", "bloomberg"}
                     and not source.get("allowed", False)})

    report = {"sources": rows, "checked": bool(check),
              "warning": "A robots/policy probe does not verify article discovery or content quality."}
    if not check:
        return report

    client = Access(config)
    try:
        for row in rows:
            if not row["enabled"] or row["kind"] != "news":
                continue
            source = sources[row["source_id"]]
            host = source["hosts"][0]
            origin = f"https://{host}"
            row["checked_at"] = datetime.now(timezone.utc).isoformat()
            try:
                client.policy(origin)
                robot = client.robot_policy(origin, source.get("min_interval_seconds", 0))
                row["status"] = "allowed" if robot.can_fetch(config["user_agent"], origin + "/") else "robots_disallowed"
            except Exception as exc:
                row["status"] = "unavailable"
                row["error"] = f"{type(exc).__name__}: {exc}"
                if host in client.paused:
                    row["status"] = "blocked"
    finally:
        client.close()
    return report
