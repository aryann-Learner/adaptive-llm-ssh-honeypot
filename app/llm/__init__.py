from __future__ import annotations

from app.config import settings
from app.honeypot.environment_profiles import EnvironmentProfiles
from app.honeypot.filesystem_generator import FilesystemGenerator


def demo_environment() -> None:
    profile = EnvironmentProfiles().get("junior_sandbox")
    generator = FilesystemGenerator(profile)
    print(f"Profile: {profile.name}")
    print(f"Base path: {profile.base_path}")
    print(generator.list_dir("/home/intern"))


if __name__ == "__main__":
    demo_environment()
    print(f"Honeypot configured for {settings.honeypot_host}:{settings.honeypot_port}")
