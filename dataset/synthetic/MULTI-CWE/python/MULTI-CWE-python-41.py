import os
import json
import sqlite3
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, Any, List


class SyncSession:
    def init(self, root: Path):
        self.root = root.resolve()
        self.input_root = (self.root / "input").resolve()
        self.output_root = (self.root / "output").resolve()
        self.state_root = (self.root / "state").resolve()
        self.key_root = (self.root / "keys").resolve()

        self.db_file = (self.state_root / "sync.sqlite3").resolve()

        self._batch: List[Dict[str, Any]] = []
        self._prepared: bool = False

    def start(self) -> None:
        self.input_root.mkdir(parents=True, exist_ok=True)
        self.output_root.mkdir(parents=True, exist_ok=True)
        self.state_root.mkdir(parents=True, exist_ok=True)
        self.key_root.mkdir(parents=True, exist_ok=True)
        self._prepared = True

    def prepare(self, payload: Dict[str, Any]) -> None:
        if not self._prepared:
            raise RuntimeError("session not started")

        items = payload.get("items", [])
        if not isinstance(items, list):
            self._batch = []
            return

        normalized: List[Dict[str, Any]] = []
        for entry in items:
            if not isinstance(entry, dict):
                continue

            name = str(entry.get("name", "")).strip()
            action = str(entry.get("action", "inspect")).strip() or "inspect"

            if not name:
                continue

            normalized.append(
                {
                    "name": name,
                    "action": action,
                }
            )

        self._batch = normalized

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def _load_targets(self, group: str) -> List[str]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT target FROM sync_targets WHERE group_name = ?",
                (group,),
            )
            return [r[0] for r in cur.fetchall()]
        finally:
            conn.close()

    def _resolve_input(self, name: str) -> Path:
        part = Path(name).name
        candidate = (self.input_root / part).resolve()
        if self.input_root not in candidate.parents and candidate != self.input_root:
            raise RuntimeError("invalid input path")
        return candidate

    def _resolve_output(self, name: str) -> Path:
        part = Path(name).name
        candidate = (self.output_root / part).resolve()
        if self.output_root not in candidate.parents and candidate != self.output_root:
            raise RuntimeError("invalid output path")
        return candidate

    def _command_for(self, action: str) -> List[str]:
        mapping = {
            "inspect": ["file", "-b"],
            "checksum": ["sha256sum"],
            "lines": ["wc", "-l"],
        }
        return list(mapping.get(action, mapping["inspect"]))

    def _execute(self, action: str, path: Path) -> Dict[str, Any]:
        command = self._command_for(action) + [str(path)]

        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return {
            "exit": proc.returncode,
            "stdout": len(proc.stdout),
            "stderr": len(proc.stderr),
        }

    def _load_key(self) -> bytes:
        env_val = os.environ.get("SYNC_KEY", "")
        if env_val:
            return env_val.encode("utf-8")

        file_path = (self.key_root / "sync.key").resolve()
        if self.key_root not in file_path.parents and file_path != self.key_root:
            return b""

        if not file_path.exists():
            return b""

        try:
            return file_path.read_bytes().strip()
        except OSError:
            return b""

    def run(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self._batch:
            return []
        group = str(payload.get("group", "")).strip()
        targets = self._load_targets(group)

        results: List[Dict[str, Any]] = []

        for item in self._batch:
            path = self._resolve_input(item["name"])
            if not path.exists():
                continue

            execution = self._execute(item["action"], path)

            results.append(
                {
                    "file": path.name,
                    "targets": len(targets),
                    "execution": execution,
                }
            )

        return results

    def flush(self, results: List[Dict[str, Any]], output_name: str) -> Dict[str, Any]:
        key = self._load_key()
        digest = hashlib.sha256(
            key + json.dumps(results, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

        output_path = self._resolve_output(output_name)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(
                {
                    "count": len(results),
                    "items": results,
                    "digest": digest,
                },
                handle,
                indent=2,
            )

        return {
            "written": str(output_path),
            "count": len(results),
        }


def run_sync_session(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/sync_session").resolve()

    try:
        payload = json.loads(request_text)
    except json.JSONDecodeError:
        return {"error": "invalid"}

    session = SyncSession(root)
    session.start()
    session.prepare(payload)

    results = session.run(payload)
    outcome = session.flush(results, str(payload.get("output", "sync.json")).strip())

    return outcome