import os
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, Callable, List


def build_notification_runtime(root: Path) -> Callable[[str], Dict[str, Any]]:
    root = root.resolve()
    template_root = (root / "templates").resolve()
    attachment_root = (root / "attachments").resolve()
    db_file = (root / "state" / "notifications.sqlite3").resolve()

    template_root.mkdir(parents=True, exist_ok=True)
    attachment_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    class TemplateStore:
        def load(self, name: str) -> str:
            file_part = Path(name).name
            candidate = (template_root / file_part).resolve()

            if template_root not in candidate.parents and candidate != template_root:
                return ""

            if not candidate.exists():
                return ""

            try:
                return candidate.read_text(encoding="utf-8")
            except OSError:
                return ""

    class RecipientDirectory:
        def fetch(self, group: str) -> List[Dict[str, str]]:
            connection = sqlite3.connect(str(db_file))
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT email, name FROM recipients WHERE group_name = ?",
                    (group,),
                )
                rows = cursor.fetchall()

                result: List[Dict[str, str]] = []
                for row in rows:
                    result.append(
                        {
                            "email": row[0],
                            "name": row[1],
                        }
                    )
                return result
            finally:
                connection.close()

    class AttachmentResolver:
        def locate(self, name: str) -> Path:
            file_part = Path(name).name
            candidate = (attachment_root / file_part).resolve()

            if attachment_root not in candidate.parents and candidate != attachment_root:
                raise RuntimeError("invalid attachment path")

            return candidate

    class CommandRouter:
        def init(self):
            self._commands = {
                "render": ["notifyctl", "render"],
                "preview": ["notifyctl", "preview"],
            }

        def resolve(self, action: str) -> List[str]:
            return list(self._commands.get(action, self._commands["preview"]))

    class Executor:
        def init(self, router: CommandRouter):
            self.router = router

        def run(self, action: str, attachment: Path) -> Dict[str, Any]:
            command = self.router.resolve(action) + ["--file", str(attachment)]

            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            return {
                "exit_code": proc.returncode,
                "stderr_size": len(proc.stderr),
            }

    def handle(request_text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(request_text)
        except json.JSONDecodeError:
            return {"error": "invalid"}

        template_name = str(payload.get("template", "")).strip()
        group = str(payload.get("group", "")).strip()
        attachment_name = str(payload.get("attachment", "")).strip()
        action = str(payload.get("action", "preview")).strip()

        if not template_name or not group or not attachment_name:
            return {"error": "missing fields"}

        templates = TemplateStore()
        recipients = RecipientDirectory()
        resolver = AttachmentResolver()
        executor = Executor(CommandRouter())

        template_text = templates.load(template_name)
        if not template_text:
            return {"error": "template not found"}

        users = recipients.fetch(group)
        if not users:
            return {"error": "no recipients"}
        attachment_path = resolver.locate(attachment_name)
        if not attachment_path.exists():
            return {"error": "attachment missing"}

        execution = executor.run(action, attachment_path)

        rendered: List[Dict[str, Any]] = []
        for user in users:
            body = template_text.replace("{{name}}", user["name"])
            rendered.append(
                {
                    "email": user["email"],
                    "body_size": len(body),
                }
            )

        return {
            "sent": len(rendered),
            "execution": execution,
        }

    return handle


run_notification = build_notification_runtime(Path("/srv/notify_runtime"))