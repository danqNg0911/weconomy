"""Bounded Katana discovery from configured category pages."""
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import yaml
from lxml import etree, html

from .access import Access, canonical_url
from .progress import heartbeat


def load_collection(path: Path) -> dict:
    settings = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    targets = settings.get("targets")
    crawl = settings.get("crawl", {})
    if not isinstance(targets, list) or not targets or not isinstance(settings.get("batch_size"), int):
        raise ValueError("Collection YAML must define targets and batch_size")
    if (settings["batch_size"] < 1 or not isinstance(crawl.get("max_pages_per_target"), int)
            or crawl["max_pages_per_target"] < 1 or crawl.get("concurrency", 1) != 1
            or crawl.get("delay_seconds", 0) < 1 or not re.fullmatch(r"\d+[smh]", crawl.get("crawl_duration", "60s"))):
        raise ValueError("Collection YAML requires positive crawl limits and serial requests")
    for target in targets:
        if (not isinstance(target.get("id"), str) or not isinstance(target.get("url"), str)
                or not isinstance(target.get("source"), str) or not isinstance(target.get("article_pattern"), str)
                or not isinstance(target.get("article_link_xpath"), str) or not target["article_link_xpath"]
                or not isinstance(target.get("body_xpath"), str) or not isinstance(target.get("max_articles"), int)
                or target["max_articles"] < 1):
            raise ValueError("Every target needs id, url, source, article_link_xpath, article_pattern, body_xpath and max_articles")
        re.compile(target["article_pattern"])
        etree.XPath(target["article_link_xpath"])
    objectives = settings.get("objectives", {})
    if any(v is not None and (not isinstance(v, int) or v < 0) for v in objectives.values()):
        raise ValueError("Objectives must be nonnegative integers or null")
    if not isinstance(settings.get("max_articles"), int) or settings["max_articles"] < 1:
        raise ValueError("Collection YAML requires a positive max_articles safety cap")
    return settings


def katana_command(target: str, max_pages: int, delay_seconds: int, *, image: str = "projectdiscovery/katana:latest",
                   depth: int = 1, timeout_seconds: int = 15, max_response_bytes: int = 4_194_304,
                   robots_out_scope: list[str] | None = None,
                   crawl_scope: str | None = None, crawl_duration: str = "30s",
                   display_out_of_scope: bool = False) -> list[str]:
    parsed_target = urlsplit(canonical_url(target))
    host = parsed_target.hostname
    command = ["docker", "run", "--rm", image, "-u", target, "-d", str(depth),
               "-crawl-scope", crawl_scope or rf"https?://{re.escape(host)}{re.escape(parsed_target.path)}(?:[/?#]|$)",
               "-field-scope", "fqdn", "-mdp", str(max_pages), "-c", "1", "-p", "1",
               "-ct", crawl_duration, "-rd", str(delay_seconds), "-timeout", str(timeout_seconds),
               "-mrs", str(max_response_bytes), "-iqp", "-j", "-silent"]
    if display_out_of_scope:
        command.append("-do")
    for pattern in robots_out_scope or []:
        command.extend(["-crawl-out-scope", pattern])
    return command


def parse_katana_output(output: str) -> list[dict]:
    rows = []
    for line in output.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid Katana JSONL output") from exc
        if not isinstance(row, dict) or not isinstance(row.get("request"), dict):
            raise ValueError("Katana JSONL row lacks request details")
        endpoint = row["request"].get("endpoint")
        if not isinstance(endpoint, str):
            raise ValueError("Katana JSONL row lacks request.endpoint")
        rows.append(row)
    return rows


def select_article_urls(rows: list[dict], target: str, article_pattern: str, limit: int, *,
                        exclude_urls=()) -> list[str]:
    host = urlsplit(canonical_url(target)).hostname
    urls = []
    for row in rows:
        endpoint = row["request"]["endpoint"]
        try:
            url = canonical_url(endpoint)
        except ValueError:
            continue
        parsed = urlsplit(url)
        if parsed.hostname != host or not re.search(article_pattern, parsed.path, re.I):
            continue
        if url in exclude_urls:
            continue
        if url not in urls:
            urls.append(url)
        if len(urls) >= limit:
            break
    return urls


def _target_page_body(rows: list[dict], target: dict) -> str:
    target_url = canonical_url(target["url"])
    page = None
    for row in rows:
        try:
            if canonical_url(row["request"]["endpoint"]) == target_url:
                page = row
                break
        except ValueError:
            continue
    body = (page or {}).get("response", {}).get("body")
    if not isinstance(body, str) or not body:
        raise ValueError(f"Katana did not return the target page body: {target_url}")
    return body


def _category_page_links(body: str | bytes, page_url: str, target: dict) -> tuple[list[str], list[str]]:
    tree = html.fromstring(body)
    host = urlsplit(page_url).hostname
    urls, next_pages = [], []
    for href in tree.xpath(target["article_link_xpath"]):
        try:
            url = canonical_url(urljoin(page_url, href))
        except (TypeError, ValueError):
            continue
        parsed = urlsplit(url)
        if parsed.hostname == host and re.search(target["article_pattern"], parsed.path, re.I) and url not in urls:
            urls.append(url)
    for anchor in tree.xpath("//a[@href] | //*[@data-next-url or @data-url or @data-href or @formaction]"):
        labels = " ".join([anchor.get("rel", ""), anchor.get("aria-label", ""),
                           anchor.get("title", ""), anchor.get("class", ""),
                           anchor.text_content(), " ".join(anchor.xpath(".//@alt | .//@title | .//@aria-label"))])
        context = " ".join(" ".join((node.get("class", ""), node.get("id", ""),
                                    node.get("aria-label", ""))) for node in [anchor, *anchor.iterancestors()])
        next_label = re.search(r"\bnext\b|\b(?:trang\s*)?(?:sau|tiếp(?:\s+theo)?)\b", labels, re.I)
        next_class = re.search(r"(?:next[-_ ]?(?:page|pagination)|query-pagination-next)",
                               anchor.get("class", ""), re.I)
        load_more = re.search(r"\b(?:xem\s+thêm|tải\s+thêm|load\s+more|show\s+more)\b", labels, re.I)
        if (not next_class and not load_more
                and not (next_label and re.search(r"pagination|pager|page-nav", context, re.I))):
            continue
        href = next((anchor.get(name) for name in
                     ("data-next-url", "data-url", "data-href", "formaction", "href")
                     if anchor.get(name)), None)
        try:
            url = canonical_url(urljoin(page_url, href))
        except (TypeError, ValueError):
            continue
        parsed = urlsplit(url)
        if parsed.hostname == host and url != canonical_url(page_url) and url not in next_pages:
            next_pages.append(url)
    return urls, next_pages


def _unresolved_load_more(body: str | bytes, page_url: str) -> list[str]:
    tree = html.fromstring(body)
    host = urlsplit(page_url).hostname
    labels = []
    for control in tree.xpath("//a | //button | //*[@role='button']"):
        label = " ".join([control.get("aria-label", ""), control.get("title", ""),
                          control.text_content(), " ".join(control.xpath(".//@alt | .//@title | .//@aria-label"))])
        marker = " ".join((label, control.get("class", ""), control.get("id", "")))
        if not re.search(r"\b(?:xem\s+thêm|tải\s+thêm|load\s+more|show\s+more)\b", marker, re.I):
            continue
        href = next((control.get(name) for name in
                     ("data-next-url", "data-url", "data-href", "formaction", "href")
                     if control.get(name)), None)
        try:
            url = canonical_url(urljoin(page_url, href))
        except (TypeError, ValueError):
            labels.append(" ".join(label.split())[:100] or control.get("class", control.tag))
            continue
        if urlsplit(url).hostname != host:
            labels.append(" ".join(label.split())[:100] or control.get("class", control.tag))
    return list(dict.fromkeys(labels))


def _target_article_links(rows: list[dict], target: dict) -> set[str]:
    return set(_category_page_links(_target_page_body(rows, target), target["url"], target)[0])


def crawl_target(target: dict, settings: dict, *, runner=subprocess.run, access_factory=Access,
                 max_articles: int | None = None, progress=None, exclude_urls=()) -> list[str]:
    access = access_factory(settings)
    try:
        source = access.sources.get(target["source"])
        if not source or source.get("allowed") is not True:
            raise PermissionError(f"Source disabled: {target['source']}")
        host = urlsplit(canonical_url(target["url"])).hostname
        if host not in source.get("hosts", []):
            raise ValueError("Category URL host does not match its configured source")
        access.policy(target["url"])
        robot = access.robot_policy(f"https://{host}", source["min_interval_seconds"])
        if not robot.can_fetch(settings["user_agent"], target["url"]):
            raise PermissionError(f"robots.txt disallows category URL: {target['url']}")

        crawl = settings["crawl"]
        default_entry = getattr(robot, "default_entry", None)
        applicable_rules = list(getattr(default_entry, "rulelines", []))
        agent = settings["user_agent"].split("/", 1)[0].casefold()
        specific_entries = [entry for entry in getattr(robot, "entries", [])
                            if entry.applies_to(agent) and "*" not in entry.useragents]
        for entry in specific_entries:
            applicable_rules.extend(entry.rulelines)
        if not specific_entries:
            applicable_rules.extend(getattr(default_entry, "rulelines", []))
        denied = [rule.path for rule in applicable_rules if not rule.allowance and rule.path]
        denied_scope = [rf"https?://{re.escape(host)}{re.escape(path)}" for path in denied if path]
        page_target = rf"https?://{re.escape(host)}" + re.escape(urlsplit(canonical_url(target["url"])).path)
        command = katana_command(target["url"], crawl["max_pages_per_target"],
                                 crawl["delay_seconds"], image=crawl["image"], depth=crawl["depth"],
                                 timeout_seconds=crawl["timeout_seconds"],
                                 max_response_bytes=crawl["max_response_bytes"], robots_out_scope=denied_scope,
                                 crawl_scope=page_target, crawl_duration=crawl["crawl_duration"],
                                 display_out_of_scope=bool(target.get("article_link_xpath")))
        duration_value = int(crawl["crawl_duration"][:-1])
        duration_scale = {"s": 1, "m": 60, "h": 3600}[crawl["crawl_duration"][-1]]
        timeout = duration_value * duration_scale + min(crawl["timeout_seconds"] + 5, 20)
        if progress:
            progress({"event": "katana_start", "url": target["url"]})
        with heartbeat(progress, f"Katana crawl {target['url']}"):
            result = runner(command, capture_output=True, text=False, check=True, timeout=timeout)
        stdout = result.stdout.decode("utf-8", errors="replace") if isinstance(result.stdout, bytes) else result.stdout
        rows = parse_katana_output(stdout)

        if target.get("article_link_xpath"):
            body = _target_page_body(rows, target)
            page_url = canonical_url(target["url"])
            page_limit = crawl["max_pages_per_target"]
            url_limit = min(max_articles or target["max_articles"], target["max_articles"])
            visited_pages = {page_url}
            article_urls = []
            reported_load_more = set()
            for page_number in range(1, page_limit + 1):
                page_links, next_pages = _category_page_links(body, page_url, target)
                if progress:
                    for label in _unresolved_load_more(body, page_url):
                        if label not in reported_load_more:
                            progress({"event": "load_more_skipped", "target": target["id"],
                                      "url": page_url, "label": label})
                            reported_load_more.add(label)
                added = 0
                for endpoint in page_links:
                    if endpoint in article_urls or endpoint in exclude_urls:
                        continue
                    try:
                        access.policy(endpoint)
                    except PermissionError:
                        continue
                    if not robot.can_fetch(settings["user_agent"], endpoint):
                        continue
                    article_urls.append(endpoint)
                    added += 1
                    if len(article_urls) >= url_limit:
                        break
                if progress:
                    progress({"event": "category_page", "target": target["id"],
                              "page": page_number, "url": page_url, "new_articles": added,
                              "total_articles": len(article_urls)})
                if len(article_urls) >= url_limit:
                    break
                next_url = next((url for url in next_pages if url not in visited_pages), None)
                if not next_url:
                    break
                visited_pages.add(next_url)
                try:
                    with heartbeat(progress, f"Fetch category page {page_number + 1}"):
                        fetched = access.fetch(next_url)
                    if "text/html" not in fetched["headers"].get("content-type", "").lower():
                        raise ValueError("Pagination response is not HTML")
                    page_url = canonical_url(fetched["url"])
                    if urlsplit(page_url).hostname != host:
                        raise ValueError("Pagination redirected outside the target host")
                    body = fetched["body"]
                except Exception as exc:
                    if progress:
                        progress({"event": "pagination_error", "target": target["id"],
                                  "url": next_url, "error": f"{type(exc).__name__}: {exc}"})
                    break
            return article_urls

        entries = []
        for row in rows:
            endpoint = row["request"]["endpoint"]
            try:
                endpoint = canonical_url(endpoint)
            except ValueError:
                continue
            if urlsplit(endpoint).hostname != host:
                continue
            try:
                access.policy(endpoint)
            except PermissionError:
                continue
            if not robot.can_fetch(settings["user_agent"], endpoint):
                continue
            entries.append(row)
        return select_article_urls(entries, target["url"],
                                   target["article_pattern"], max_articles or target["max_articles"],
                                   exclude_urls=exclude_urls)
    finally:
        access.close()


def objective_reached(counts: dict, objectives: dict) -> bool:
    requested = {key: value for key, value in objectives.items() if value is not None}
    return bool(requested) and all(counts.get(key, 0) >= value for key, value in requested.items())


def run_collection(config_path: Path, *, runner=subprocess.run, process_fn=None, target_ids=None,
                   objectives=None, discover_only=False, progress=None, exclude_urls=(),
                   max_new_urls=None) -> dict:
    from . import pipeline

    settings = load_collection(config_path)
    if objectives is not None:
        settings["objectives"] = objectives
    settings["sources"] = str((config_path.resolve().parent / "sources.yaml").resolve())
    settings["aliases"] = str((config_path.resolve().parent.parent / settings["aliases"]).resolve())
    settings["output"] = str((config_path.resolve().parent.parent / settings["output"]).resolve())
    source_path = Path(settings["sources"])
    if not source_path.is_file():
        raise FileNotFoundError(f"Source registry missing: {source_path}")
    source_rows = yaml.safe_load(source_path.read_text(encoding="utf-8"))["sources"]
    processor = process_fn or pipeline.process
    if not discover_only and settings["ner_backend"] == "models":
        import importlib.util
        if importlib.util.find_spec("gliner") is None:
            raise RuntimeError("GLiNER is missing; install the project's nlp extra")
    targets = settings["targets"]
    if target_ids:
        unknown = set(target_ids) - {target["id"] for target in targets}
        if unknown:
            raise ValueError(f"Unknown target(s): {', '.join(sorted(unknown))}")
        targets = [target for target in targets if target["id"] in target_ids]
    if not targets:
        raise ValueError("No crawl targets selected")
    cap = min(settings["max_articles"], settings["max_documents"])
    if max_new_urls is not None:
        if max_new_urls <= 0:
            raise ValueError("max_new_urls must be positive")
        cap = min(cap, max_new_urls)
    batch_size = min(settings["batch_size"], cap, settings["max_documents"])
    failures, target_reports = [], []
    counts = {"articles": 0, "nodes": 0, "relations": 0, "relation_types": 0,
              "extracted_entities": 0, "entities": 0}
    discovered_urls = set()
    attempted_urls = set()
    accepted_article_urls = set()
    from .pipeline import read_table
    graph_nodes = set()
    graph_edges = set()
    relation_types = set()
    extracted_entity_ids = set()
    access = Access(settings)
    try:
        for target in targets:
            source = access.sources.get(target["source"])
            host = urlsplit(canonical_url(target["url"])).hostname
            if not source or source.get("allowed") is not True or host not in source.get("hosts", []):
                raise ValueError(f"Target source/host policy mismatch: {target['id']}")
    finally:
        access.close()
    configured_total = min(cap, sum(target["max_articles"] for target in targets))
    for target_index, target in enumerate(targets, 1):
        remaining = min(cap - len(attempted_urls), target["max_articles"])
        if remaining <= 0 or objective_reached(counts, settings["objectives"]):
            break
        source = source_rows.get(target["source"])
        if source is None or source.get("allowed") is not True:
            raise PermissionError(f"Source disabled: {target['source']}")
        if progress:
            progress({"event": "target_start", "index": target_index, "total": len(targets),
                      "target": target["id"], "url": target["url"]})
        try:
            target_urls = crawl_target(target, settings, runner=runner, max_articles=remaining,
                                       progress=progress, exclude_urls=set(exclude_urls) | discovered_urls)
        except Exception as exc:
            error = {"target": target["id"], "url": target["url"],
                     "error": f"{type(exc).__name__}: {exc}"}
            failures.append(error)
            target_reports.append({"id": target["id"], "discovered": 0, "processed": 0,
                                   "run_ids": [], "article_urls": [], "errors": [error]})
            if progress:
                progress({"event": "info", "message": f"Discovery failed for {target['id']}: {error['error']}"})
            continue
        target_urls = [url for url in target_urls if url not in attempted_urls]
        target_report = {"id": target["id"], "discovered": len(target_urls), "processed": 0,
                         "run_ids": [], "errors": []}
        discovered_urls.update(target_urls)
        if progress:
            progress({"event": "target_discovered", "target": target["id"],
                      "count": len(target_urls)})
        if discover_only:
            attempted_urls.update(target_urls)
            target_report["article_urls"] = target_urls
            target_report["attempted"] = len(target_urls)
            target_reports.append(target_report)
            continue
        batch_index = 0
        while len(attempted_urls.intersection(target_urls)) < len(target_urls):
            if len(attempted_urls) >= cap or objective_reached(counts, settings["objectives"]):
                break
            batch = []
            batch_limit = min(batch_size, cap - len(attempted_urls))
            for url in target_urls:
                if url in attempted_urls:
                    continue
                batch.append(url)
                if len(batch) >= batch_limit:
                    break
            if not batch:
                continue
            batch_index += 1
            attempted_urls.update(batch)
            config = {key: value for key, value in settings.items()
                      if key not in {"targets", "batch_size", "crawl", "objectives", "max_articles"}}
            config["max_documents"] = max(config["max_documents"], len(batch))
            config["sources"] = settings["sources"]
            config["aliases"] = settings["aliases"]
            config["output"] = settings["output"]
            config["user_agent"] = settings["user_agent"]
            config["min_article_words"] = settings["min_article_words"]
            config["min_text_chars"] = settings["min_text_chars"]
            config["request_timeout"] = settings["request_timeout"]
            config["max_response_bytes"] = settings["max_response_bytes"]
            config["delay_seconds"] = max(source.get("min_interval_seconds", 0), settings["crawl"]["delay_seconds"])
            if progress:
                progress({"event": "batch_start", "target": target["id"], "index": batch_index,
                          "size": len(batch), "attempted": len(attempted_urls), "cap": cap})
            options = {"source_overrides": {target["source"]: {"body_xpath": target["body_xpath"],
                                                                 "language": target["language"]}}}
            if process_fn is None:
                options["progress"] = (lambda event: progress({**event, "stage": "crawl",
                                                               "target": target["id"]})) if progress else None
            with heartbeat(progress, f"Đang xử lý batch {batch_index} của {target['id']}"):
                run, report = processor(config, urls=batch, **options)
            target_report["run_ids"].append(str(run))
            target_report["processed"] += len(batch)
            target_report["attempted"] = target_report.get("attempted", 0) + len(batch)
            failures.extend(report.get("errors", []))
            article_rows = report.get("article_rows") if process_fn is not None else None
            article_rows = article_rows if article_rows is not None else read_table(run, "articles")
            counts["attempted"] = len(attempted_urls)
            accepted_article_urls.update(
                row["canonical_url"] for row in article_rows
                if row.get("content_status") == "body_checked" and not row.get("duplicate_of")
            )
            counts["articles"] = len(accepted_article_urls)
            relation_rows = read_table(run, "relations")
            entities = read_table(run, "entities")
            graph_nodes.update(endpoint for row in relation_rows
                               for endpoint in (row["subject_id"], row["object_id"]))
            graph_edges.update((row["subject_id"], row["predicate"], row["object_id"])
                               for row in relation_rows)
            relation_types.update(row["predicate"] for row in relation_rows)
            extracted_entity_ids.update(entity["entity_id"] for entity in entities)
            counts["extracted_entities"] = len(extracted_entity_ids)
            counts["entities"] = len(extracted_entity_ids)
            counts["nodes"] = len(graph_nodes)
            counts["relations"] = len(graph_edges)
            counts["relation_types"] = len(relation_types)
            if progress:
                progress({"event": "batch_done", "target": target["id"], "index": batch_index,
                          "processed": len(batch), "counts": dict(counts)})
        target_report["errors"] = [error for error in failures if error.get("url") in target_urls]
        target_reports.append(target_report)
    if (not discover_only and not failures
            and any(value is not None for value in settings["objectives"].values())
            and not objective_reached(counts, settings["objectives"])):
        failures.append({"error": "Configured targets or article safety cap were exhausted before all objectives were met"})
    return {"status": "completed" if not failures else "partial", "counts": counts,
            "objectives": settings["objectives"], "objectives_met": objective_reached(counts, settings["objectives"]),
            "note": "entities counts resolved entity rows; nodes counts distinct relation endpoints only",
            "max_articles": cap, "attempted_urls": len(attempted_urls),
            "discovered_urls": len(discovered_urls), "configured_target_capacity": configured_total,
            "articles_remaining": max(0, cap - len(attempted_urls)),
            "targets": target_reports, "errors": failures}
