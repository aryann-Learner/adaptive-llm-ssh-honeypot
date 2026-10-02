# Adaptive LLM SSH Honeypot

An adaptive LLM-driven SSH honeypot that simulates a cluttered, lived-in Linux sandbox for red-team research and attacker behavior capture.

## Goals

- Simulate a believable junior developer environment on Ubuntu 22.04
- Capture reconnaissance, command sequencing, credential harvesting, and prompt-injection attempts
- Generate realistic shell responses based on attacker behavior and prior activity
- Provide a flexible environment profile system for different low-value targets
- Record attacker activity without assuming production security integrity

## Design principles

- The target should feel real, messy, and under-defended.
- The environment should be dynamic rather than static.
- Shell responses should be contextual and inconsistent in ways that feel human.
- LLM-driven outputs should assist in realism while preserving a clean evidence trail.
- The honeypot should only expose enough intent to attract noise and low-skill attacks.

## Included environment profile

This project ships with a default sandbox profile modeled after a junior developer VM:

- `/home/intern`
- `notes.txt` with half-finished reminders
- `todo.txt` with tasks and incomplete ideas
- `.bash_history` showing learning loops and repeated commands
- `test123.py` using debug prints and experimental code
- `node_modules/` left behind in an abandoned state
- weak permissions and non-production conventions
- realistic terminal prompts and shell behavior

## Architecture

- `app/honeypot/environment_profiles.py` defines the realistic target profiles
- `app/honeypot/filesystem_generator.py` generates a living filesystem description
- `app/honeypot/attacker_behavior.py` evaluates suspicious sequences and adapts realism
- `app/honeypot/ssh_server.py` is the SSH interaction layer
- `app/llm/client.py` connects to an LLM provider for dynamic responses
- `app/storage/*` records sessions and events for threat analysis

## Quick start

1. Create a virtual environment
2. Install dependencies
3. Copy `.env.example` to `.env` and set your LLM provider settings
4. Run the honeypot entrypoint

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Environment variables

See `.env.example` for the supported configuration keys.

## Example threat coverage

- `ls`, `pwd`, `whoami`, `id`
- `find / -maxdepth 3`
- `cat /etc/passwd`, `/etc/shadow` probing
- attempted credential harvesting near home directories
- shell history inspection
- prompt injection in a local CLI assistant or shell wrapper
- traversal through `/tmp`, `/var/www`, or project directories

## Safety and ethics

This project is intended for defensive security research, red-team environment emulation, and controlled attack capture. It should only be run in isolated lab or sandbox environments with explicit authorization.

## Repo status

This is an initial scaffold intended to provide a realistic starting point. It is designed to be extended with a real SSH server implementation, prompt-injection detection logic, and event storage for later analysis.
