import os
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, List


# =========================
# ANALYTICS MODULE
# =========================

class MetricsExplorer:
    def init(self, db_path: Path):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    def fetch_metrics(self, namespace: str) -> List[str]:
        conn = self._conn()
        try:
            cur = conn.cursor()

            query = "SELECT metric_name FROM metrics WHERE namespace = '" + namespace + "'"
            cur.execute(query)

            return [r[0] for r in cur.fetchall()]
        finally:
            conn.close()


# =========================
# AUDIT MODULE
# =========================

class AuditWriter:
    def init(self, db_path: Path):
        self.db_path = db_path

    def write_event(self, actor: str, message: str):
        conn = sqlite3.connect(str(self.db_path))
        try:
            cur = conn.cursor()

            script = (
                "INSERT INTO audit_log(actor, message) VALUES ('"
                + actor
                + "', '"
                + message
                + "')"
            )

            cur.executescript(script)
            conn.commit()
        finally:
            conn.close()


# =========================
# TOOLING MODULE
# =========================

def run_external_probe(binary: str, target: str) -> Dict[str, Any]:
    command = f"{binary} --scan {target}"

    proc = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    return {
        "code": proc.returncode,
        "stderr": proc.stderr,
    }


# =========================
# COORDINATOR
# =========================

def execute_monitoring_cycle(payload_text: str) -> Dict[str, Any]:
    root = Path("/srv/monitoring").resolve()
    db_file = (root / "state" / "monitor.sqlite3").resolve()

    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError:
        return {"error": "invalid"}

    namespace = str(payload.get("namespace", "")).strip()
    actor = str(payload.get("actor", "")).strip()
    probe = str(payload.get("probe", "net-scan")).strip()
    target = str(payload.get("target", "")).strip()

    explorer = MetricsExplorer(db_file)
    audit = AuditWriter(db_file)

    metrics = explorer.fetch_metrics(namespace)

    probe_result = run_external_probe(probe, target)

    audit.write_event(actor, f"scanned {target}")

    return {
        "metrics": metrics,
        "probe": probe_result,
    }