from __future__ import annotations

import socketserver
import threading
import time
from typing import Any, Dict

import paramiko
from paramiko import AUTH_FAILED, AUTH_SUCCESSFUL, OPEN_SUCCEEDED, Channel, ServerInterface, Transport

from app.config import settings
from app.honeypot.environment_profiles import EnvironmentProfiles
from app.honeypot.filesystem_generator import FilesystemGenerator


class HoneypotServerHandler(ServerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.event = None
        self.username = ""
        self.cwd = "/home/intern"
        self.history: list[str] = []
        self.fs = FilesystemGenerator(EnvironmentProfiles().get("junior_sandbox"))

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username: str, password: str) -> int:
        accepted_usernames = {settings.default_username, "admin", "root"}
        accepted_passwords = {settings.default_password, "admin", "Password123", "123456"}
        if username in accepted_usernames and password in accepted_passwords:
            self.username = username
            return AUTH_SUCCESSFUL
        return AUTH_FAILED

    def check_auth_publickey(self, username: str, key) -> bool:
        return False

    def check_channel_shell_request(self, channel: Channel) -> bool:
        channel.send(b"Welcome to the sandbox.\n")
        return True

    def check_channel_exec_request(self, channel: Channel, command: str) -> bool:
        channel.send(f"Command received: {command}\n".encode())
        return True


class ParamikoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        transport = Transport(self.request)
        transport.add_server_key(self.server.host_key)
        transport.start_server(server=HoneypotServerHandler())

        channel = transport.accept(20)
        if channel is None:
            return

        channel.settimeout(1.0)
        try:
            while transport.is_active():
                time.sleep(0.1)
        except Exception:
            pass
        finally:
            channel.close()
            transport.close()


class SSHHoneypotServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address: tuple[str, int], handler_class: type[ParamikoRequestHandler]) -> None:
        self.host_key = paramiko.RSAKey.generate(2048)
        super().__init__(server_address, handler_class)
        self._server_thread = None

    def start(self) -> None:
        self._server_thread = threading.Thread(target=self.serve_forever, daemon=True)
        self._server_thread.start()


def start_server() -> None:
    server = SSHHoneypotServer((settings.honeypot_host, settings.honeypot_port), ParamikoRequestHandler)
    server.start()
    print(f"SSH honeypot listening on {settings.honeypot_host}:{settings.honeypot_port}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
