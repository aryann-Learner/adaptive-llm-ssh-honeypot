from __future__ import annotations

from app.models import LLMResponse


class ResponseAdapter:
    def adapt(self, raw_text: str, *, suspicious: bool = False, prompt_injection: bool = False) -> LLMResponse:
        return LLMResponse(
            text=raw_text.strip(),
            confidence=0.82 if suspicious else 0.66,
            detected_prompt_injection=prompt_injection,
            suspicious_actions=["credential_access_attempt"] if suspicious else [],
        )
