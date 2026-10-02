from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FileNode(BaseModel):
    path: str
    content: str = ""
    permissions: str = "0644"
    directory: bool = False


class SessionEvent(BaseModel):
    timestamp: str
    session_id: str
    event_type: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ShellInteraction(BaseModel):
    session_id: str
    command: str
    cwd: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    suspicious: bool = False
    prompt_injection: bool = False
    events: List[str] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)


class EnvironmentProfile(BaseModel):
    name: str
    description: str
    base_path: str
    files: List[FileNode] = Field(default_factory=list)
    defaults: Dict[str, Any] = Field(default_factory=dict)
    shell_prompt: str = "intern@dev-sandbox:~$ "
    banner: str = "Ubuntu 22.04 LTS"


class LLMResponse(BaseModel):
    text: str
    confidence: Optional[float] = None
    detected_prompt_injection: bool = False
    suspicious_actions: List[str] = Field(default_factory=list)
