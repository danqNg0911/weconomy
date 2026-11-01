from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Settings(BaseModel):
    user_agent: str = "AcademicNewsCollector/0.1"
    timeout_seconds: float = Field(20, gt=0)
    delay_seconds: float = Field(3, ge=0)
    max_retries: int = Field(2, ge=0, le=5)
    max_response_bytes: int = Field(10_000_000, gt=0)
    target_per_source: int = Field(10, ge=1, le=10)
    max_attempts_per_source: int = Field(30, ge=1)
    max_articles_per_source: int = Field(10, ge=1, le=10)
    max_consecutive_restricted: int = Field(3, ge=1)
    max_urls_per_source: int = Field(100, ge=1)
    max_sitemaps: int = Field(6, ge=1)
    max_sitemap_roots: int = Field(2, ge=1)
    max_sitemap_depth: int = Field(2, ge=0)
    min_words: int = Field(100, ge=1)
    data_dir: Path = Path("data")


def load(config_dir: Path):
    settings = Settings(**yaml.safe_load((config_dir / "settings.yaml").read_text("utf-8")))
    sources = yaml.safe_load((config_dir / "sources.yaml").read_text("utf-8"))["sources"]
    keywords = yaml.safe_load((config_dir / "keywords.yaml").read_text("utf-8"))["keywords"]
    return settings, sources, keywords
