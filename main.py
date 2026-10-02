from __future__ import annotations

from app.config import settings
from app.honeypot.ssh_server import start_server


if __name__ == "__main__":
    start_server()
