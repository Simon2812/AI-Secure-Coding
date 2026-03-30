import os
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class AccountStore:
    def __init__(self, db_file: Path):
        self.db_file = db_file

    def find_user(self, username: str) -> Dict[str, Any]:
        conn = sqlite3.connect(str(self.db_file))
        try:
            cur = conn.cursor()

            query = (
                "SELECT id, username, role "
                "FROM users "
                "WHERE username = '" + username + "'"
            )

            cur.execute(query)
            row = cur.fetchone()

            if not row:
                return {}

            return {
                "id": row[0],
                "username": row[1],
                "role": row[2],
            }
        finally:
            conn.close()


class FileManager:
    def __init__(self, root: Path):
        self.root = root

    def load_profile(self, name: str) -> Dict[str, Any]:
        target = self.root / name

        if not target.exists():
            return {}

        try:
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}


class TaskRunner:
    def run(self, action: str, resource: str) -> Dict[str, Any]:
        cmd = f"{action} {resource}"

        proc = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
        )

        return {
            "code": proc.returncode,
            "out": proc.stdout[:100],
        }


class KeyProvider:
    def get(self) -> bytes:
        return b"internal-default-key"


def _parse(text: str) -> Dict[str, Any]:
    try:
        obj = json.loads(text)
    except Exception:
        return {}
    return obj if isinstance(obj, dict) else {}


def run_service(request_text: str) -> Dict[str, Any]:
    base = Path("/srv/account_service")
    db_file = base / "state" / "users.db"
    profile_root = base / "profiles"

    profile_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    payload = _parse(request_text)

    username = str(payload.get("username", "")).strip()
    profile_name = str(payload.get("profile", "")).strip()
    action = str(payload.get("action", "ls")).strip()
    resource = str(payload.get("resource", "")).strip()

    if not username:
        return {"error": "missing username"}

    store = AccountStore(db_file)
    user = store.find_user(username)

    if not user:
        return {"error": "not found"}

    manager = FileManager(profile_root)
    profile = manager.load_profile(profile_name)

    runner = TaskRunner()
    execution = runner.run(action, resource)

    key = KeyProvider().get()

    return {
        "user": user["username"],
        "profile": profile,
        "execution": execution,
        "key_len": len(key),
    }