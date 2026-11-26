from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(REPO_ROOT / ".env", ROOT / ".env"),
        extra="ignore",
    )
    database_url: str = ""
    create_tables: bool = False
    mock_delay: float = Field(default=0.02, ge=0, le=0.1)
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    chat_mode: Literal["llm", "mock"] = "llm"
    llm_provider: Literal["openai", "cloudflare"] = "openai"
    cloudflare_account_id: str = Field(default="", pattern=r"^(?:[a-fA-F0-9]{32})?$")
    cloudflare_api_token: SecretStr = SecretStr("")
    cloudflare_model: str = "@cf/swiss-ai/apertus-v1.5-8b"
    openai_api_key: SecretStr = SecretStr("")
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = ""
    openai_api_mode: Literal["chat", "responses"] = "chat"
    openai_reasoning_effort: str = ""
    openai_reasoning_summary: str = ""
    neo4j_uri: str = ""
    neo4j_username: str = ""
    neo4j_user: str = "neo4j"
    neo4j_password: SecretStr = SecretStr("")
    neo4j_database: str = "neo4j"
    graph_max_hops: int = Field(default=3, ge=1, le=4)
    graph_max_seeds: int = Field(default=4, ge=1, le=8)
    graph_neighbors_per_node: int = Field(default=8, ge=1, le=20)
    graph_max_nodes: int = Field(default=60, ge=5, le=150)
    graph_max_edges: int = Field(default=100, ge=5, le=250)
    evidence_index_path: str = str(ROOT / ".data" / "evidence.sqlite3")
    llm_max_output_tokens: int = Field(default=1024, ge=128, le=4096)
    llm_history_messages: int = Field(default=6, ge=1, le=100)
    llm_system_prompt: str = (
        "Bạn là trợ lý Weconomy. Trả lời rõ ràng bằng ngôn ngữ người dùng. "
        "Chỉ hỗ trợ kinh tế và đầu tư quốc tế. Dựa vào dữ liệu đồ thị được cung cấp; "
        "phân biệt dữ kiện và suy luận, không bịa quan hệ hay nguồn trích dẫn."
    )

    @model_validator(mode="after")
    def configure_provider(self):
        if self.llm_provider == "cloudflare":
            self.openai_base_url = (
                f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/ai/v1"
                if self.cloudflare_account_id
                else ""
            )
            self.openai_api_key = self.cloudflare_api_token
            self.openai_model = self.cloudflare_model
            self.openai_api_mode = "chat"
            self.openai_reasoning_effort = ""
            self.openai_reasoning_summary = ""
        return self
