import os
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path


DB_PATH = "/opt/infra/nodes.db"
REPORT_DIR = Path("/var/reports/diagnostics").resolve()


class NodeRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_node(self, node_id: int):
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT hostname, role, environment FROM nodes WHERE id = ?",
                (node_id,),
            )
            row = cur.fetchone()
            if not row:
                return None

            return {
                "hostname": row[0],
                "role": row[1],
                "environment": row[2],
            }
        finally:
            conn.close()


class DiagnosticRunner:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _build_report_path(self, node_id: int) -> Path:
        file_name = f"node_{node_id}_{int(datetime.utcnow().timestamp())}.log"
        return (self.base_dir / file_name).resolve()

    def _ensure_dir(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def run(self, hostname: str, mode: str) -> str:
        command = f"ping -c 1 {hostname} && echo MODE={mode}"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def save_report(self, path: Path, content: str):
        if self.base_dir not in path.parents:
            raise RuntimeError("invalid report path")

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)


def generate_diagnostic(node_id: int, mode: str) -> dict:
    repo = NodeRepository(DB_PATH)
    runner = DiagnosticRunner(REPORT_DIR)

    node = repo.get_node(node_id)
    if not node:
        return {"error": "node not found"}

    runner._ensure_dir()

    output = runner.run(node["hostname"], mode)

    report_path = runner._build_report_path(node_id)
    runner.save_report(report_path, output)

    return {
        "node": node["hostname"],
        "environment": node["environment"],
        "report": str(report_path),
        "length": len(output),
    }


def main():
    node_id = int(os.environ.get("NODE_ID", "1"))
    mode = os.environ.get("MODE", "basic")

    result = generate_diagnostic(node_id, mode)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()