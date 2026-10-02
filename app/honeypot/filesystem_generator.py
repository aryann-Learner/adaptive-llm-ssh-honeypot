from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

from app.models import EnvironmentProfile, FileNode


class FilesystemGenerator:
    def __init__(self, profile: EnvironmentProfile):
        self.profile = profile

    def generate_tree(self) -> Dict[str, object]:
        tree: Dict[str, object] = {}
        for node in self.profile.files:
            path = Path(node.path)
            relative = path.relative_to(Path(self.profile.base_path).anchor if path.is_absolute() else Path("."))
            self._insert(tree, relative.parts, {"path": str(path), "directory": node.directory, "permissions": node.permissions, "content": node.content})
        return tree

    def _insert(self, root: dict, parts: Iterable[str], value: dict) -> None:
        current = root
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value

    def list_dir(self, directory: str) -> List[str]:
        matches = []
        for file in self.profile.files:
            p = Path(file.path)
            if str(p.parent) == directory:
                matches.append(p.name)
        return sorted(matches)

    def read_file(self, path: str) -> str:
        for file in self.profile.files:
            if file.path == path:
                return file.content
        raise FileNotFoundError(path)
