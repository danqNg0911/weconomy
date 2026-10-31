import asyncio
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated

import typer
from rich import print

from .config import load
from .models import now
from .pipeline import execute
from .storage import Store

app = typer.Typer(no_args_is_help=True, help="Feasibility pilot: at most 10 saved articles per source in this database.")
config_dir = Path("configs")


@app.callback()
def main(config: Annotated[Path, typer.Option(help="Directory containing YAML files")] = Path("configs")):
    global config_dir
    config_dir = config


@contextmanager
def writer_lock(root: Path):
    """OS lock releases on crash; do not delete the lock file."""
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".writer.lock").open("a+b") as handle:
        handle.write(b"0")
        handle.flush()
        handle.seek(0)
        import os
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise typer.BadParameter("Another crawler process is using this data directory") from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def invoke(action, source, all_sources, method="both", limit=None, max_attempts=None, max_consecutive_restricted=None):
    settings, sources, keywords = load(config_dir)
    if source and all_sources:
        raise typer.BadParameter("Use --source or --all, not both")
    if source and source not in sources:
        raise typer.BadParameter(f"Unknown source: {source}")
    if method not in {"rss", "sitemap", "both"}:
        raise typer.BadParameter("method must be rss, sitemap or both")
    target = limit if limit is not None else settings.target_per_source
    if not 1 <= target <= 10:
        raise typer.BadParameter("Pilot limit must be 1..10, per source")
    with writer_lock(settings.data_dir):
        asyncio.run(execute(settings, sources, keywords, config_dir,
                            [source] if source else list(sources), action, method, target, max_attempts, max_consecutive_restricted))


@app.command()
def init_db():
    settings, _, _ = load(config_dir)
    with writer_lock(settings.data_dir):
        store = Store(settings.data_dir)
        store.db.close()
    print(f"Initialized {settings.data_dir / 'crawler.db'}")


@app.command()
def validate_sources(source: str | None = None, all: bool = False):
    """Probe endpoints, save evidence/config and enqueue discovered URLs; no article downloads."""
    invoke("validate", source, all)


@app.command()
def discover(source: str | None = None, all: bool = False, method: str = "both"):
    invoke("discover", source, all, method)


@app.command()
def run(source: str | None = None, all: bool = False, method: str = "both", max_articles: int = 10,
        max_attempts: int | None = None, max_consecutive_restricted: int | None = None,
        limit: int | None = typer.Option(None, hidden=True, help="Deprecated alias for --max-articles")):
    """Discover and fetch until each source has LIMIT successful articles (maximum 10)."""
    invoke("run", source, all, method, limit if limit is not None else max_articles, max_attempts, max_consecutive_restricted)


@app.command()
def fetch(source: str | None = None, all: bool = False, max_articles: int = 10,
          max_attempts: int | None = None, max_consecutive_restricted: int | None = None):
    invoke("fetch", source, all, limit=max_articles, max_attempts=max_attempts, max_consecutive_restricted=max_consecutive_restricted)


@app.command()
def stats():
    settings, _, _ = load(config_dir)
    with writer_lock(settings.data_dir):
        store = Store(settings.data_dir)
        print(json.dumps(store.stats(), ensure_ascii=False, indent=2))
        store.db.close()


@app.command()
def export(format: str = "jsonl"):
    if format != "jsonl":
        raise typer.BadParameter("Only jsonl is supported")
    settings, _, _ = load(config_dir)
    with writer_lock(settings.data_dir):
        store = Store(settings.data_dir)
        print(str(store.export()))
        store.db.close()


@app.command()
def retry_failed(source: str | None = None):
    """Requeue transient fetch/extraction errors; respect Retry-After and retry budget."""
    settings, sources, _ = load(config_dir)
    if source and source not in sources:
        raise typer.BadParameter("Unknown source")
    with writer_lock(settings.data_dir):
        store = Store(settings.data_dir)
        with store.db:
            cursor = store.db.execute('''UPDATE url_queue SET status='pending'
                WHERE status IN ('fetch_failed','extraction_failed')
                AND (http_status IS NULL OR http_status=200 OR http_status=429 OR http_status>=500)
                AND (next_retry_at IS NULL OR julianday(next_retry_at)<=julianday(?))
                AND retry_count<3 AND (? IS NULL OR source_id=?)''', (now(), source, source))
        print(f"Requeued {cursor.rowcount}; run fetch to continue")
        store.db.close()


if __name__ == "__main__":
    app()
