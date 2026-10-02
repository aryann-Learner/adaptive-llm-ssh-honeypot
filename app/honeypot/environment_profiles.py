from __future__ import annotations

from app.models import EnvironmentProfile


class EnvironmentProfiles:
    def __init__(self) -> None:
        self.profile_map = {
            "junior_sandbox": self._junior_sandbox(),
        }

    def _junior_sandbox(self) -> EnvironmentProfile:
        from app.prompts import DEFAULT_ENVIRONMENT

        return DEFAULT_ENVIRONMENT

    def get(self, name: str) -> EnvironmentProfile:
        try:
            return self.profile_map[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Unknown profile: {name}") from exc
