from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    honeypot_host: str = os.getenv("HONEYPOT_HOST", "0.0.0.0")
    honeypot_port: int = int(os.getenv("HONEYPOT_PORT", "2222"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    session_storage_path: str = os.getenv("SESSION_STORAGE_PATH", "./data/sessions")
    event_log_path: str = os.getenv("EVENT_LOG_PATH", "./data/events.jsonl")
    ssh_banner: str = os.getenv("SSH_BANNER", "Ubuntu 22.04 LTS")
    default_username: str = os.getenv("DEFAULT_USERNAME", "intern")
    default_password: str = os.getenv("DEFAULT_PASSWORD", "password123")
    llm_request_timeout: float = float(os.getenv("LLM_REQUEST_TIMEOUT_SECONDS", "12.0"))
    llm_daily_budget_usd: float = float(os.getenv("LLM_DAILY_BUDGET_USD", "5.0"))


settings = Settings()
