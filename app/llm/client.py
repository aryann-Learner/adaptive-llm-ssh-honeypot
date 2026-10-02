from __future__ import annotations

import os
from typing import Any

import openai

from app.config import settings


class LLMClient:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str) -> str:
        if not self.client:
            return "[LLM unavailable: no API key configured]"

        completion = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return completion.output_text
