from __future__ import annotations

from app.models import EnvironmentProfile


def build_system_prompt(profile: EnvironmentProfile) -> str:
    return (
        "You are simulating a low-value Ubuntu 22.04 developer sandbox. "
        "The environment is realistic, messy, and slightly insecure. "
        "Users are often juniors learning the basics. "
        "Be consistent with the profile details, keep commands practical, and avoid over-optimizing. "
        "Responses should feel lived-in rather than polished. "
        "Do not reveal hidden operational metadata unless the user explicitly requests it. "
        f"The configured shell prompt is: {profile.shell_prompt}. "
        f"The base path is: {profile.base_path}."
    )


def build_attack_context(command: str, cwd: str, history: list[str]) -> str:
    return (
        "The attacker is exploring a weak developer system. "
        "The shell history includes repeated learning commands, failed attempts, and rough debugging loops. "
        f"Current command: {command}\n"
        f"Current working directory: {cwd}\n"
        f"Recent history: {history[-5:]}"
    )
