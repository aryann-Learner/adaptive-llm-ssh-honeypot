from __future__ import annotations

import os
from typing import Dict, List

from app.llm.client import LLMClient


class SessionState:
    """Tracks mutable session state: CWD, VFS mutations, history."""

    def __init__(self, username: str = "intern", hostname: str = "dev-sandbox") -> None:
        self.username = username
        self.hostname = hostname
        self.cwd = f"/home/{username}"
        
        # In-memory virtual filesystem: {path: content}
        self.vfs: Dict[str, str] = {
            "/etc/os-release": 'NAME="Ubuntu"\nVERSION="22.04.3 LTS (Jammy Jellyfish)"\n',
            "/etc/hostname": f"{hostname}\n",
            "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\nintern:x:1000:1000:intern:/home/intern:/bin/bash\n",
            f"/home/{username}/notes.txt": "TODO:\n- finish the SSH notes\n- ask about cron job setup\n- find the right nginx config\n- maybe fix permissions later\n- don't forget to backup the DB\n- still trying to understand systemd\n",
            f"/home/{username}/todo.txt": "- [ ] test the API\n- [ ] revisit nginx config\n- [ ] fix broken script\n- [ ] check git status again\n- [ ] do not run as root\n",
            f"/home/{username}/.bash_history": "ls\ncd /tmp\nls -la\nchmod 777 /tmp/*\nwhoami\ncd ~\nls\npython3 test123.py\ncat notes.txt\n",
            f"/home/{username}/test123.py": "print('starting test')\nprint('checking env')\nprint('still debugging')\nprint('not sure why this fails')\nprint('maybe this is the issue')\n",
        }
        self.history: List[str] = []
        self.llm_client = LLMClient()

    def get_prompt(self) -> str:
        """Return shell prompt based on current state."""
        if self.cwd == f"/home/{self.username}" or self.cwd == f"/root":
            display_path = "~"
        else:
            display_path = self.cwd
        
        symbol = "#" if self.username == "root" else "$"
        return f"{self.username}@{self.hostname}:{display_path}{symbol} "

    def _normalize_path(self, path: str) -> str:
        """Resolve path relative to current working directory."""
        if path.startswith("/"):
            return os.path.normpath(path)
        return os.path.normpath(os.path.join(self.cwd, path))

    def execute_command(self, cmd_line: str) -> str:
        """Execute a command, handling state mutations locally where possible."""
        self.history.append(cmd_line)
        parts = cmd_line.strip().split(None, 1)
        if not parts:
            return ""
        
        cmd = parts[0]
        args_str = parts[1] if len(parts) > 1 else ""
        args = args_str.split() if args_str else []

        # === Local deterministic commands ===
        
        if cmd == "pwd":
            return self.cwd

        if cmd == "whoami":
            return self.username

        if cmd == "hostname":
            return self.hostname

        if cmd == "cd":
            target = args[0] if args else f"/home/{self.username}"
            if target == "~":
                target = f"/home/{self.username}"
            new_path = self._normalize_path(target)
            self.cwd = new_path
            return ""

        if cmd == "touch" and args:
            filepath = self._normalize_path(args[0])
            if filepath not in self.vfs:
                self.vfs[filepath] = ""
            return ""

        if cmd == "cat" and args:
            filepath = self._normalize_path(args[0])
            if filepath in self.vfs:
                return self.vfs[filepath]
            return f"cat: {filepath}: No such file or directory"

        if cmd == "ls" or cmd == "ls -la":
            # Simple mock: list files in current directory
            cwd_files = []
            for path in self.vfs.keys():
                parent = os.path.dirname(path)
                if parent == self.cwd:
                    cwd_files.append(os.path.basename(path))
            
            if not cwd_files:
                return ""
            
            # Format as simple ls output
            if cmd == "ls -la":
                output_lines = ["-rw-r--r-- 1 intern intern 1024 Oct  9 12:00 " + f for f in sorted(cwd_files)]
            else:
                output_lines = sorted(cwd_files)
            
            return "\n".join(output_lines)

        if cmd == "echo" and args:
            return " ".join(args)

        if cmd == "id":
            uid = 0 if self.username == "root" else 1000
            gid = 0 if self.username == "root" else 1000
            return f"uid={uid}({self.username}) gid={gid}({self.username}) groups={gid}"

        if cmd == "uname" and (not args or args[0] in ["-a", "-s"]):
            return "Linux"

        if cmd == "exit" or cmd == "logout":
            return "[SESSION_EXIT]"

        # === Fallback to LLM for complex commands ===
        return self.call_llm_with_state(cmd_line)

    def call_llm_with_state(self, cmd_line: str) -> str:
        """Invoke LLM enriched with current session context."""
        # Build context injection
        state_context = f"""Current session state:
- User: {self.username}
- Hostname: {self.hostname}
- CWD: {self.cwd}
- Files in VFS: {list(self.vfs.keys())}
- Command history: {self.history[-5:]}  (last 5 commands)
"""
        
        prompt = f"""{state_context}

The user just typed: {cmd_line}

Respond with ONLY the raw terminal output this command would produce on Ubuntu 22.04. 
Do not break character. Do not explain. Output only what the shell would output."""
        
        try:
            response = self.llm_client.generate(prompt)
            return response
        except Exception:
            # Graceful fallback: mock response
            return f"{cmd_line}: command not found"
