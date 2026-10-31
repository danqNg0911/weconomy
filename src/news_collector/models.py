from datetime import datetime, timezone

from pydantic import BaseModel, Field, HttpUrl


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Article(BaseModel):
    article_id: str
    source: str
    url: HttpUrl
    canonical_url: HttpUrl
    title: str = Field(min_length=1)
    description: str | None = None
    authors: list[str] = Field(default_factory=list)
    published_at: str | None = None
    updated_at: str | None = None
    collected_at: str = Field(default_factory=now)
    language: str
    category: str | None = None
    tags: list[str] = Field(default_factory=list)
    content: str = Field(min_length=1)
    word_count: int
    content_hash: str
    discovery_method: str
    discovery_endpoint: str
    extraction_method: str
    extraction_version: str = "0.1"
    http_status: int = 200
    crawl_status: str = "success"
    relevance_status: str = "review"
    relevance_score: int = 0
    matched_keywords: list[str] = Field(default_factory=list)
    quality_flags: list[str] = Field(default_factory=list)
    topic_scope: str = "uncertain"
    geographic_scope: str = "uncertain"
    duplicate_of: str | None = None
    raw_file_path: str | None = None
