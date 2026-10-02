from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class SessionStore:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_session(self, session_id: str, payload: Dict[str, Any]) -> Path:
        session_path = self.storage_dir / f"{session_id}.json"
        with session_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
        return session_path

    def load_session(self, session_id: str) -> Dict[str, Any]:
        session_path = self.storage_dir / f"{session_id}.json"
        with session_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
