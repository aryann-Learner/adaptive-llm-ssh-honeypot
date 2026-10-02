from __future__ import annotations

import os
from typing import Any

import openai

from app.config import settings


class LLMClient:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        self.request_timeout = float(settings.llm_request_timeout)
        self.daily_budget_usd = float(settings.llm_daily_budget_usd)
        self._daily_spend_usd = 0.0
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str) -> str:
        if not self.client:
            return "[LLM unavailable: no API key configured]"
        if self._daily_spend_usd >= self.daily_budget_usd:
            return "[LLM unavailable: daily spend budget exceeded]"

        try:
            completion = self.client.responses.create(
                model=self.model,
                input=prompt,
                timeout=self.request_timeout,
            )
        except Exception:
            return "[LLM unavailable: request failed]"

        output_text = getattr(completion, "output_text", "")
        self._daily_spend_usd += 0.01
        return output_text or ""
