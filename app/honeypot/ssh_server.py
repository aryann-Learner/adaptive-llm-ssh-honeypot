from __future__ import annotations

import socketserver
import threading
from typing import Any, Dict

from paramiko import AUTH_FAILED, AUTH_SUCCESSFUL, AutoAddPolicy, Channel, ServerInterface
from paramiko import Transport

from app.config import settings
from app.honeypot.environment_profiles import EnvironmentProfiles
from app.honeypot.filesystem_generator import FilesystemGenerator


class HoneypotServerHandler(ServerInterface):
    def __init__(self) -> None:
        self.event = None
        self.username = ""
        self.cwd = "/home/intern"
        self.history: list[str] = []
        self.fs = FilesystemGenerator(EnvironmentProfiles().get("junior_sandbox"))

    def check_channel_request(self, kind: str, chanid: int) -> bool:
        return True

    def check_auth_password(self, username: str, password: str) -> bool:
        return username == settings.default_username and password == settings.default_password

    def check_auth_publickey(self, username: str, key) -> bool:
        return False

    def check_channel_shell_request(self, channel: Channel) -> bool:
        return True

    def check_channel_exec_request(self, channel: Channel, command: str) -> bool:
        return True


class SSHHoneypotServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address: tuple[str, int], handler_class: type[HoneypotServerHandler]) -> None:
        super().__init__(server_address, handler_class)
        self._server_thread = None

    def start(self) -> None:
        self._server_thread = threading.Thread(target=self.serve_forever, daemon=True)
        self._server_thread.start()


def start_server() -> None:
    # Real SSH implementation is intentionally scaffolded for extension.
    # This entrypoint prepares the environment for integration with paramiko.
    server = SSHHoneypotServer((settings.honeypot_host, settings.honeypot_port), HoneypotServerHandler)
    server.start()
    print(f"SSH honeypot listening on {settings.honeypot_host}:{settings.honeypot_port}")
