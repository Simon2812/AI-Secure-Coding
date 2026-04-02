import os
import json
import sqlite3
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, Callable, List


class EventBus:
    def init(self):
        self._handlers: Dict[str, List[Callable[[Dict[str, Any]], Dict[str, Any]]]] = {}

    def on(self, event: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for handler in self._handlers.get(event, []):
            results.append(handler(payload))
        return results


class Store:
    def init(self, db_file: Path):
        self.db_file = db_file

    def _conn(self):
        return sqlite3.connect(str(self.db_file))

    def resolve_targets(self, group: str) -> List[str]:
        conn = self._conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT target FROM dispatch_targets WHERE group_name = ?",
                (group,),
            )
            return [r[0] for r in cur.fetchall()]
        finally:
            conn.close()


class FileSpace:
    def init(self, base: Path):
        self.base = base.resolve()

    def input_file(self, name: str) -> Path:
        part = Path(name).name
        candidate = (self.base / part).resolve()
        if self.base not in candidate.parents and candidate != self.base:
            raise RuntimeError("invalid input path")
        return candidate

    def output_file(self, name: str) -> Path:
        part = Path(name).name
        candidate = (self.base / part).resolve()
        if self.base not in candidate.parents and candidate != self.base:
            raise RuntimeError("invalid output path")
        return candidate


class ToolSet:
    def init(self):
        self._mapping = {
            "inspect": ["file", "-b"],
            "checksum": ["sha256sum"],
        }

    def resolve(self, action: str) -> List[str]:
        return list(self._mapping.get(action, self._mapping["inspect"]))


class Runner:
    def init(self, tools: ToolSet):
        self.tools = tools

    def execute(self, action: str, path: Path) -> Dict[str, Any]:
        command = self.tools.resolve(action) + [str(path)]

        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return {
            "exit": proc.returncode,
            "out": len(proc.stdout),
            "err": len(proc.stderr),
        }


class KeyProvider:
    def init(self, root: Path):
        self.root = root.resolve()

    def load(self) -> bytes:
        env_val = os.environ.get("DISPATCH_KEY", "")
        if env_val:
            return env_val.encode("utf-8")

        file_path = (self.root / "dispatch.key").resolve()
        if self.root not in file_path.parents and file_path != self.root:
            return b""

        if not file_path.exists():
            return b""

        try:
            return file_path.read_bytes().strip()
        except OSError:
            return b""


def build_event_runtime(root: Path) -> Callable[[str], Dict[str, Any]]:
    root = root.resolve()
    input_root = (root / "input").resolve()
    output_root = (root / "output").resolve()
    state_root = (root / "state").resolve()

    input_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)
    state_root.mkdir(parents=True, exist_ok=True)

    db_file = (state_root / "dispatch.sqlite3").resolve()

    store = Store(db_file)
    fs_in = FileSpace(input_root)
    fs_out = FileSpace(output_root)
    runner = Runner(ToolSet())
    key_provider = KeyProvider(root)

    bus = EventBus()

    def on_collect(payload: Dict[str, Any]) -> Dict[str, Any]:
        group = str(payload.get("group", "")).strip()
        targets = store.resolve_targets(group)
        return {"targets": targets}
    def on_process(payload: Dict[str, Any]) -> Dict[str, Any]:
        source_name = str(payload.get("source", "")).strip()
        action = str(payload.get("action", "inspect")).strip()

        path = fs_in.input_file(source_name)
        if not path.exists():
            return {"error": "missing input"}

        result = runner.execute(action, path)
        return {"result": result, "file": path.name}

    def on_finalize(payload: Dict[str, Any]) -> Dict[str, Any]:
        output_name = str(payload.get("output", "result.json")).strip()
        data = payload.get("data", {})

        key = key_provider.load()
        digest = hashlib.sha256(key + json.dumps(data, separators=(",", ":")).encode("utf-8")).hexdigest()

        output_path = fs_out.output_file(output_name)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump({"data": data, "digest": digest}, handle, indent=2)

        return {"written": str(output_path)}

    bus.on("collect", on_collect)
    bus.on("process", on_process)
    bus.on("finalize", on_finalize)

    def handle(request_text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(request_text)
        except json.JSONDecodeError:
            return {"error": "invalid"}

        collect_res = bus.emit("collect", payload)
        process_res = bus.emit("process", payload)

        merged = {
            "targets": collect_res[0].get("targets", []) if collect_res else [],
            "execution": process_res[0].get("result", {}) if process_res else {},
        }

        finalize_res = bus.emit(
            "finalize",
            {
                "output": payload.get("output", ""),
                "data": merged,
            },
        )

        return {
            "targets": len(merged["targets"]),
            "execution": merged["execution"],
            "output": finalize_res[0].get("written") if finalize_res else None,
        }

    return handle


run_dispatch = build_event_runtime(Path("/srv/event_dispatch"))