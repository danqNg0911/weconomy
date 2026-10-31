import json
import uuid
from pathlib import Path

import yaml
from rich.console import Console

from .discovery import candidates, inspect_endpoint
from .extraction import extract
from .fetching import Client, CrawlError
from .models import now
from .storage import Store

console = Console(markup=False)


async def execute(settings, sources: dict, keywords: list[str], config_dir: Path,
                  selected: list[str], action: str, method: str = "both", target: int = 10,
                  max_attempts: int | None = None, max_consecutive_restricted: int | None = None):
    store, client = Store(settings.data_dir), Client(settings)
    run_id = uuid.uuid4().hex
    report = {"run_id": run_id, "started_at": now(), "action": action,
              "target_per_source": target, "sources": {}}
    with store.db:
        store.db.execute("INSERT INTO crawl_runs VALUES(?,?,NULL,'running',NULL)", (run_id, now()))
        for key, source in sources.items():
            store.db.execute("INSERT OR REPLACE INTO sources VALUES(?,?)", (key, json.dumps(source)))
    try:
        for key in selected:
            source = sources[key]
            console.print(f"[{key}] {action}: {store.count(key)}/{target} articles already saved")
            result = {"discovered": 0, "new_urls": 0, "attempted": 0, "fetched": 0, "extracted": 0, "restricted": 0, "relevant": 0, "saved_this_run": 0,
                      "endpoints": [], "errors": []}
            report["sources"][key] = result
            if action in {"validate", "discover", "run"} and not (action == "run" and store.count(key) >= target):
                endpoints, errors = await candidates(client, source)
                result["errors"].extend(errors)
                verified = []
                seen = set()
                for endpoint in endpoints:
                    if method != "both" and endpoint["method"] != method:
                        continue
                    console.print(f"[{key}] checking {endpoint['method']}: {endpoint['url']}")
                    entries, evidence = await inspect_endpoint(client, source, endpoint)
                    result["endpoints"].extend(evidence)
                    first = evidence[0] if evidence else {"status": "unknown"}
                    verified.append(dict(endpoint, status=first["status"], last_checked_at=now(),
                                         last_error=first.get("error")))
                    with store.db:
                        for item in evidence:
                            store.db.execute("INSERT OR REPLACE INTO discovery_endpoints VALUES(?,?,?)",
                                             (item["url"], key, json.dumps(item)))
                    # A bounded queue; retain all provenance for URLs already seen.
                    bounded = []
                    for entry in entries:
                        if entry["url"] in seen or len(seen) < settings.max_urls_per_source:
                            bounded.append(entry)
                            seen.add(entry["url"])
                    result["discovered"] += len(bounded)
                    result["new_urls"] += store.enqueue(key, bounded)
                    # Run prioritizes a working RSS feed; validate checks all candidates.
                    if action != "validate" and len(seen) >= settings.max_attempts_per_source:
                        break
                statuses = [e["status"] for e in verified]
                source["status"] = ("available" if "available" in statuses else "restricted"
                                    if "restricted" in statuses or any(e["status"] == "restricted" for e in errors)
                                    else "unavailable" if statuses else "unknown")
                previous = {(e["url"], e["method"]): e for e in source.get("endpoints", [])}
                previous.update({(e["url"], e["method"]): e for e in verified})
                source["endpoints"] = list(previous.values())
                source["last_checked_at"] = now()
                source["last_errors"] = errors
            result["discovery_status"] = source.get("status", "unknown")
            result["fetch_status"] = "unknown"
            result["extraction_status"] = "unknown"
            result["relevance_status"] = "unknown"
            if action in {"run", "fetch"}:
                attempt_cap = max_attempts or settings.max_attempts_per_source
                pending = store.db.execute("SELECT * FROM url_queue WHERE source_id=? AND status='pending' ORDER BY discovered_at,url LIMIT ?",
                                           (key, attempt_cap)).fetchall()
                restricted_streak = 0
                for row in pending:
                    if store.count(key) >= target or result["attempted"] >= attempt_cap:
                        break
                    url = row["url"]
                    store.state(url, "fetching")
                    result["attempted"] += 1
                    try:
                        response = await client.get(url, source["base_url"])
                        result["fetched"] += 1
                        article = extract(response.content, str(response.url), key, source,
                                          json.loads(row["metadata"]), keywords, settings.min_words)
                        result["extracted"] += 1
                        result["relevant"] += article.relevance_status == "relevant"
                        restricted_streak = 0
                        if store.save(article, url):
                            result["saved_this_run"] += 1
                            safe_title = article.title.encode("ascii", "replace").decode("ascii")
                            console.print(f"[{key}] {store.count(key)}/{target} {safe_title}", markup=False)
                    except (CrawlError, ValueError, TypeError) as exc:
                        status = exc.status if isinstance(exc, CrawlError) else "extraction_failed"
                        if status == "restricted":
                            result["restricted"] += 1
                            restricted_streak += 1
                        else:
                            restricted_streak = 0
                        http_status = exc.http_status if isinstance(exc, CrawlError) else 200
                        retry_at = exc.retry_at if isinstance(exc, CrawlError) else None
                        store.state(url, status, str(exc), http_status, retry_at)
                        result["errors"].append({"url": url, "status": status, "error": str(exc), "diagnostics": getattr(exc, "diagnostics", [])})
                        with store.db:
                            store.db.execute("INSERT INTO crawl_errors(run_id,url,error_type,message,created_at) VALUES(?,?,?,?,?)",
                                             (run_id, url, status, str(exc), now()))
                        console.print(f"[{key}] {status}: {exc}", markup=False)
                        if http_status == 429 or restricted_streak >= (max_consecutive_restricted or settings.max_consecutive_restricted):
                            result["pause_reason"] = "max_consecutive_restricted" if restricted_streak else "rate_limited"
                            break
                result["fetch_status"] = "restricted" if result["restricted"] and not result["fetched"] else "available" if result["fetched"] else "unavailable"
                result["extraction_status"] = "available" if result["extracted"] else "failed"
                result["relevance_status"] = "available" if result["extracted"] else "unknown"
            result["saved_total"] = store.count(key)
            result["target_reached"] = store.count(key) >= target
            console.print(f"[{key}] complete: {store.count(key)}/{target}; discovery={result.get('discovery_status')}; fetch={result.get('fetch_status')}")
        report["status"] = "completed"
    except BaseException:
        report["status"] = "interrupted"
        raise
    finally:
        report["finished_at"] = now()
        report["statistics"] = store.stats()
        report["robots"] = client.robots_evidence
        directory = settings.data_dir / "reports"
        directory.mkdir(parents=True, exist_ok=True)
        output = directory / f"{run_id}.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2), "utf-8")
        (directory / "latest.json").write_text(output.read_text("utf-8"), "utf-8")
        with store.db:
            store.db.execute("UPDATE crawl_runs SET finished_at=?,status=?,report=? WHERE run_id=?",
                             (now(), report["status"], str(output), run_id))
        if action in {"validate", "discover", "run"}:
            path = config_dir / "sources.yaml"
            temporary = path.with_suffix(".tmp")
            temporary.write_text(yaml.safe_dump({"sources": sources}, allow_unicode=True, sort_keys=False), "utf-8")
            temporary.replace(path)
        store.export()
        store.db.close()
        await client.close()
        console.print(f"Report: {output}")
    return report
