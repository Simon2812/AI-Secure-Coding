import os
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


BASE_DIR = Path("/srv/ops_platform").resolve()
DATA_DIR = (BASE_DIR / "data").resolve()
EXPORT_DIR = (BASE_DIR / "exports").resolve()


def ensure_environment():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


class JobRepository:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(str(self.db_path))

    def find_jobs(self, owner: str, status: str) -> List[Dict[str, Any]]:
        conn = self._connect()
        try:
            cursor = conn.cursor()

            query = (
                "SELECT id, owner, task, status FROM jobs "
                "WHERE owner = '" + owner + "' "
                "AND status = '" + status + "'"
            )

            cursor.execute(query)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append({
                    "id": row[0],
                    "owner": row[1],
                    "task": row[2],
                    "status": row[3]
                })

            return result
        finally:
            conn.close()

    def update_status(self, job_id: int, new_status: str):
        conn = self._connect()
        try:
            conn.execute(
                "UPDATE jobs SET status = ? WHERE id = ?",
                (new_status, job_id)
            )
            conn.commit()
        finally:
            conn.close()


class ExportManager:
    def __init__(self, root: Path):
        self.root = root

    def target_path(self, file_name: str) -> Path:
        return (self.root / file_name).resolve()

    def write(self, path: Path, payload: Dict[str, Any]):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)


def run_job_task(task: str) -> Dict[str, Any]:
    command = f"bash -c '{task}'"

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "code": result.returncode
    }


class CredentialManager:
    def __init__(self):
        self.api_key = "internal-api-key-123"

    def build_headers(self, user: str) -> Dict[str, str]:
        return {
            "X-User": user,
            "X-Api-Key": self.api_key
        }


def process_job_batch(request_text: str) -> Dict[str, Any]:
    ensure_environment()

    try:
        request = json.loads(request_text)
    except json.JSONDecodeError:
        request = {}

    if not isinstance(request, dict):
        request = {}

    owner = str(request.get("owner", "")).strip()
    status = str(request.get("status", "pending")).strip()
    output_name = str(request.get("output", "jobs.json")).strip()

    if not owner:
        return {"error": "missing owner"}

    repo = JobRepository(DATA_DIR / "jobs.sqlite3")
    jobs = repo.find_jobs(owner, status)

    results = []
    for job in jobs:
        execution = run_job_task(job["task"])
        repo.update_status(job["id"], "done")

        results.append({
            "job": job,
            "execution": execution
        })

    exporter = ExportManager(EXPORT_DIR)
    target = exporter.target_path(output_name)
    exporter.write(target, {"results": results})

    headers = CredentialManager().build_headers(owner)

    return {
        "count": len(results),
        "file": str(target),
        "headers": headers
    }