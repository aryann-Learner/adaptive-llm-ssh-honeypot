from __future__ import annotations

import re
from typing import List

from app.models import ShellInteraction


class AttackerBehaviorAnalyzer:
    def __init__(self) -> None:
        self.suspicious_patterns = [
            r"cat\s+/etc/passwd",
            r"ls\s+-la\s+/home",
            r"find\s+/\s+-maxdepth",
            r"grep\s+-R\s+\"password\"",
            r"curl\s+.*http",
            r"wget\s+.*http",
            r"chmod\s+777",
            r"nc\s+-l",
            r"ssh\s+.*@",
        ]

    def evaluate(self, command: str) -> tuple[bool, bool, List[str]]:
        suspicious = False
        prompt_injection = False
        events: List[str] = []
        normalized = command.strip()

        if re.search(
            r"(ignore previous instructions|ignore prior instructions|system prompt|developer mode|override the system prompt|bypass the instructions)",
            normalized,
            re.IGNORECASE,
        ):
            prompt_injection = True
            suspicious = True
            events.append("prompt_injection_detected")

        if any(re.search(pattern, normalized, re.IGNORECASE) for pattern in self.suspicious_patterns):
            suspicious = True
            events.append("suspicious_command")

        if re.search(r"cat\s+.*(id_rsa|\.ssh|authorized_keys|shadow)", normalized, re.IGNORECASE):
            suspicious = True
            events.append("credential_harvest_attempt")

        return suspicious, prompt_injection, events

    def build_interaction(self, session_id: str, command: str, cwd: str, history: List[str]) -> ShellInteraction:
        suspicious, prompt_injection, events = self.evaluate(command)
        recent_history = list(history[-25:])
        return ShellInteraction(
            session_id=session_id,
            command=command,
            cwd=cwd,
            stdout="",
            stderr="",
            exit_code=0,
            suspicious=suspicious,
            prompt_injection=prompt_injection,
            events=events,
            history=recent_history,
        )
