import os
import json
import subprocess
import sqlite3
from pathlib import Path
from typing import Dict, List, Any


class MetricsReader:
    def __init__(self, db_file: Path):
        self.db_file = db_file

    def read_for_host(self, host: str) -> List[Dict[str, Any]]:
        connection = sqlite3.connect(str(self.db_file))
        try:
            cursor = connection.cursor()

            query = (
                "SELECT metric, value, created_at "
                "FROM host_metrics "
                "WHERE host = '" + host + "' "
                "ORDER BY created_at DESC LIMIT 50"
            )

            cursor.execute(query)
            rows = cursor.fetchall()

            result: List[Dict[str, Any]] = []
            for row in rows:
                result.append(
                    {
                        "metric": row[0],
                        "value": row[1],
                        "created_at": row[2],
                    }
                )
            return result
        finally:
            connection.close()


class SnapshotWriter:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def prepare(self):
        self.root.mkdir(parents=True, exist_ok=True)

    def target_file(self, name: str) -> Path:
        return (self.root / name).resolve()

    def write(self, path: Path, payload: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)


def collect_system_info(extra: str) -> Dict[str, str]:
    command = f"uname -a && {extra}"

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode
    }


def build_snapshot(host: str, metrics: List[Dict[str, Any]], sysinfo: Dict[str, str]) -> Dict[str, Any]:
    return {
        "host": host,
        "metric_count": len(metrics),
        "metrics": metrics,
        "system": {
            "output_size": len(sysinfo["stdout"]),
            "exit_code": sysinfo["exit_code"]
        }
    }


def execute_snapshot(request: Dict[str, Any]) -> Dict[str, Any]:
    host = str(request.get("host", "")).strip()
    extra = str(request.get("extra_cmd", "")).strip()
    output_name = str(request.get("output", "snapshot.json")).strip()

    if not host:
        return {"error": "missing host"}

    reader = MetricsReader(Path("/var/infra/metrics.sqlite3"))
    metrics = reader.read_for_host(host)

    sysinfo = collect_system_info(extra)

    snapshot = build_snapshot(host, metrics, sysinfo)

    writer = SnapshotWriter(Path("/var/infra/snapshots"))
    writer.prepare()

    target = writer.target_file(output_name)
    writer.write(target, snapshot)

    return {
        "written_to": str(target),
        "metric_count": len(metrics)
    }


def run_from_env():
    raw = os.environ.get("SNAPSHOT_REQUEST", "{}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {}

    if not isinstance(data, dict):
        data = {}

    return execute_snapshot(data)