from __future__ import annotations

from app.models import EnvironmentProfile, FileNode


DEFAULT_ENVIRONMENT = EnvironmentProfile(
    name="junior_sandbox",
    description="A lived-in Ubuntu 22.04 sandbox for a junior developer with weak permissions and confusing setup choices.",
    base_path="/home/intern",
    shell_prompt="intern@dev-sandbox:~$ ",
    banner="Ubuntu 22.04 LTS",
    files=[
        FileNode(path="/home/intern/notes.txt", content="TODO:\n- finish the SSH notes\n- ask about cron job setup\n- find the right nginx config\n- maybe fix permissions later\n- don't forget to backup the DB\n- still trying to understand systemd\n"),
        FileNode(path="/home/intern/todo.txt", content="- [ ] test the API\n- [ ] revisit nginx config\n- [ ] fix broken script\n- [ ] check git status again\n- [ ] do not run as root\n"),
        FileNode(path="/home/intern/.bash_history", content="ls\ncd /tmp\nls -la\nchmod 777 /tmp/*\nwhoami\ncd ~\nls\npython3 test123.py\ncat notes.txt\nfailed git clone attempt\n"),
        FileNode(path="/home/intern/test123.py", content="print('starting test')\nprint('checking env')\nprint('still debugging')\nprint('not sure why this fails')\nprint('maybe this is the issue')\n"),
        FileNode(path="/home/intern/node_modules", content="", directory=True),
        FileNode(path="/home/intern/creds_backup.txt", content="username=admin\npassword=Summer2024!\nendpoint=https://internal.example.local/api\n"),
    ],
    defaults={
        "user": "intern",
        "host": "dev-sandbox",
        "os": "Ubuntu 22.04",
        "privilege": "user",
    },
)
