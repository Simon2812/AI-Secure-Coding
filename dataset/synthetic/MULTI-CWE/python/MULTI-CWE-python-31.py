import os
import json
import gzip
import shutil
import sqlite3
import tempfile
import subprocess
from pathlib import Path
from collections import deque
from typing import Dict, Any, Iterable, List, Tuple, Callable


def build_probe_runtime(root: Path) -> Callable[[str], Dict[str, Any]]:
    root = root.resolve()
    profile_root = (root / "profiles").resolve()
    trace_root = (root / "traces").resolve()
    report_root = (root / "reports").resolve()
    work_root = (root / "work").resolve()
    state_db = (root / "state" / "agent.sqlite3").resolve()

    def ensure_layout() -> None:
        profile_root.mkdir(parents=True, exist_ok=True)
        trace_root.mkdir(parents=True, exist_ok=True)
        report_root.mkdir(parents=True, exist_ok=True)
        work_root.mkdir(parents=True, exist_ok=True)
        state_db.parent.mkdir(parents=True, exist_ok=True)

    def parse_request(text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def normalize_jobs(raw: object) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = []
        if not isinstance(raw, list):
            return items

        for entry in raw:
            if not isinstance(entry, dict):
                continue

            probe_id = str(entry.get("probe_id", "")).strip()
            target = str(entry.get("target", "")).strip()
            tool = str(entry.get("tool", "netprobe")).strip() or "netprobe"
            trace_name = str(entry.get("trace_name", "")).strip()
            hook = str(entry.get("hook", "")).strip()

            if not probe_id or not target or not trace_name:
                continue

            items.append(
                {
                    "probe_id": probe_id,
                    "target": target,
                    "tool": tool,
                    "trace_name": trace_name,
                    "hook": hook,
                }
            )

        return items

    def clamp_limit(value: object) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError):
            return 20

        if number < 1:
            return 1
        if number > 150:
            return 150
        return number

    def open_db() -> sqlite3.Connection:
        connection = sqlite3.connect(str(state_db))
        connection.execute(
            "CREATE TABLE IF NOT EXISTS probe_runs ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "probe_id TEXT NOT NULL, "
            "target TEXT NOT NULL, "
            "status TEXT NOT NULL, "
            "created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
        connection.commit()
        return connection

    def load_profile(name: str) -> Dict[str, Any]:
        profile_file = (profile_root / f"{Path(name).name}.json").resolve()
        if not profile_file.exists():
            return {}

        try:
            with open(profile_file, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

        return payload if isinstance(payload, dict) else {}

    def allocate_workspace(batch_name: str) -> Path:
        workspace = Path(tempfile.mkdtemp(prefix=f"{Path(batch_name).name}_", dir=str(work_root))).resolve()
        if work_root not in workspace.parents and workspace != work_root:
            raise RuntimeError("invalid workspace")
        return workspace

    def stage_trace(trace_name: str, workspace: Path) -> Path:
        source = (trace_root / Path(trace_name).name).resolve()
        if not source.exists():
            raise FileNotFoundError(trace_name)

        staged = (workspace / source.name).resolve()
        shutil.copy2(source, staged)
        return staged
    def run_probe(tool: str, target: str, workspace: Path) -> Dict[str, Any]:
        command = f"{tool} --json {target}"
        completed = subprocess.run(
            command,
            shell=True,
            cwd=str(workspace),
            capture_output=True,
            text=True,
        )

        parsed: Dict[str, Any]
        try:
            parsed = json.loads(completed.stdout) if completed.stdout.strip() else {}
        except json.JSONDecodeError:
            parsed = {}

        return {
            "exit_code": completed.returncode,
            "stdout_size": len(completed.stdout),
            "stderr_size": len(completed.stderr),
            "payload": parsed,
        }

    def rotate_trace(trace_file: Path, post_rotate: str) -> Dict[str, Any]:
        command = f"gzip -f {trace_file} && {post_rotate}"
        exit_code = os.system(command)
        gz_name = f"{trace_file.name}.gz"

        return {
            "exit_code": exit_code,
            "rotated_file": gz_name,
        }

    def collect_recent_runs(connection: sqlite3.Connection, probe_ids: Iterable[str]) -> List[Tuple[str, str]]:
        cursor = connection.cursor()
        seen = deque(maxlen=50)

        for probe_id in probe_ids:
            cursor.execute(
                "SELECT probe_id, status FROM probe_runs WHERE probe_id = ? ORDER BY id DESC LIMIT 1",
                (probe_id,),
            )
            row = cursor.fetchone()
            if row:
                seen.append((row[0], row[1]))

        return list(seen)

    def record_run(connection: sqlite3.Connection, probe_id: str, target: str, status: str) -> None:
        connection.execute(
            "INSERT INTO probe_runs(probe_id, target, status) VALUES (?, ?, ?)",
            (probe_id, target, status),
        )
        connection.commit()

    def write_batch_report(workspace: Path, batch_name: str, rows: List[Dict[str, Any]], previous: List[Tuple[str, str]]) -> Path:
        report_file = (report_root / f"{Path(batch_name).name}.json").resolve()
        payload = {
            "batch_name": batch_name,
            "generated_rows": rows,
            "previous_runs": [
                {
                    "probe_id": probe_id,
                    "status": status,
                }
                for probe_id, status in previous
            ],
        }

        with open(report_file, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

        copy_path = (workspace / "report_copy.json").resolve()
        with open(copy_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

        return report_file

    def execute(text: str) -> Dict[str, Any]:
        ensure_layout()

        payload = parse_request(text)
        if not payload:
            return {"error": "invalid request"}

        batch_name = str(payload.get("batch_name", "probe_batch")).strip() or "probe_batch"
        profile_name = str(payload.get("profile", "default")).strip() or "default"
        limit = clamp_limit(payload.get("limit"))

        profile = load_profile(profile_name)
        requested_jobs = normalize_jobs(payload.get("jobs", []))
        selected_jobs = requested_jobs[:limit]

        if not selected_jobs:
            return {"error": "no jobs"}

        workspace = allocate_workspace(batch_name)
        results: List[Dict[str, Any]] = []

        try:
            with open_db() as connection:
                previous = collect_recent_runs(connection, [item["probe_id"] for item in selected_jobs])

                for item in selected_jobs:
                    staged_trace = stage_trace(item["trace_name"], workspace)
                    probe_result = run_probe(item["tool"], item["target"], workspace)
                    rotation_result = rotate_trace(staged_trace, item["hook"])
                    status = "ok" if probe_result["exit_code"] == 0 and rotation_result["exit_code"] == 0 else "failed"
                    record_run(connection, item["probe_id"], item["target"], status)

                    results.append(
                        {
                            "probe_id": item["probe_id"],
                            "target": item["target"],
                            "profile": profile.get("name", profile_name),
                            "probe": probe_result,
                            "rotation": rotation_result,
                        }
                    )

                report_file = write_batch_report(workspace, batch_name, results, previous)

            return {
                "batch_name": batch_name,
                "profile": profile.get("name", profile_name),
                "count": len(results),
                "report": str(report_file),
            }
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

    return execute


run_probe_batch = build_probe_runtime(Path("/srv/probe_runtime"))