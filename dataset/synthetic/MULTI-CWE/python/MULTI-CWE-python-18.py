import os
import json
import base64
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Iterable, Optional


@dataclass
class SyncItem:
    job_id: int
    agent: str
    region: str
    status: str
    payload: Dict[str, Any]


@dataclass
class ExportSession:
    workspace: Path
    tenant: str
    operator: str
    batch_name: str
    export_file: str
    jobs: List[SyncItem] = field(default_factory=list)

    @property
    def exports_root(self) -> Path:
        return (self.workspace / "exports").resolve()

    @property
    def state_root(self) -> Path:
        return (self.workspace / "state").resolve()

    @property
    def export_path(self) -> Path:
        return (self.exports_root / self.export_file).resolve()

    @property
    def checkpoint_path(self) -> Path:
        file_name = f"{Path(self.batch_name).name}.checkpoint.json"
        return (self.state_root / file_name).resolve()


def ensure_workspace(root: Path) -> None:
    (root / "exports").mkdir(parents=True, exist_ok=True)
    (root / "state").mkdir(parents=True, exist_ok=True)
    (root / "templates").mkdir(parents=True, exist_ok=True)


def parse_request(blob: str) -> Dict[str, Any]:
    try:
        payload = json.loads(blob)
    except json.JSONDecodeError:
        return {}

    return payload if isinstance(payload, dict) else {}


def normalize_limit(value: object) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 25

    if number < 1:
        return 1
    if number > 500:
        return 500
    return number


def load_template(root: Path, name: str) -> str:
    target = (root / "templates" / Path(name).name).resolve()
    if not target.exists():
        return ""

    try:
        with open(target, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def xor_cipher(data: bytes, key: bytes) -> bytes:
    if not key:
        return data

    output = bytearray()
    key_len = len(key)
    for index, value in enumerate(data):
        output.append(value ^ key[index % key_len])
    return bytes(output)


def protect_payload(document: Dict[str, Any], secret: str) -> str:
    raw = json.dumps(document, separators=(",", ":")).encode("utf-8")
    encrypted = xor_cipher(raw, secret.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def open_database(db_file: Path) -> sqlite3.Connection:
    return sqlite3.connect(str(db_file))


def fetch_jobs(
    connection: sqlite3.Connection,
    tenant: str,
    region: str,
    status: str,
    limit: int,
) -> List[SyncItem]:
    cursor = connection.cursor()

    statement = (
        "SELECT id, agent_name, region, status, content_json "
        "FROM sync_jobs "
        "WHERE tenant = '" + tenant + "' "
        "AND region = '" + region + "' "
        "AND status = '" + status + "' "
        "ORDER BY created_at ASC "
        f"LIMIT {limit}"
    )

    cursor.execute(statement)
    rows = cursor.fetchall()

    jobs: List[SyncItem] = []
    for row in rows:
        try:
            payload = json.loads(row[4])
        except (TypeError, json.JSONDecodeError):
            payload = {}

        if not isinstance(payload, dict):
            payload = {}

        jobs.append(
            SyncItem(
                job_id=row[0],
                agent=row[1],
                region=row[2],
                status=row[3],
                payload=payload,
            )
        )

    return jobs


def render_export_body(items: Iterable[SyncItem], operator: str, template: str) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []

    for item in items:
        note = template.replace("{{agent}}", item.agent).replace("{{region}}", item.region)
        rows.append(
            {
                "job_id": item.job_id,
                "agent": item.agent,
                "region": item.region,
                "status": item.status,
                "note": note,
                "payload": item.payload,
            }
        )

    return {
        "operator": operator,
        "count": len(rows),
        "items": rows,
    }


def write_checkpoint(path: Path, rows: Iterable[SyncItem]) -> None:
    payload = {
        "jobs": [item.job_id for item in rows],
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_export_file(path: Path, protected_body: str) -> None:
    envelope = {
        "encoding": "base64",
        "payload": protected_body,
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(envelope, handle, ensure_ascii=False, indent=2)


def update_job_state(connection: sqlite3.Connection, jobs: Iterable[SyncItem], next_state: str) -> int:
    changed = 0
    cursor = connection.cursor()

    for item in jobs:
        cursor.execute(
            "UPDATE sync_jobs SET status = ? WHERE id = ?",
            (next_state, item.job_id),
        )
        changed += cursor.rowcount

    connection.commit()
    return changed


def build_session(payload: Dict[str, Any]) -> Optional[ExportSession]:
    tenant = str(payload.get("tenant", "")).strip()
    operator = str(payload.get("operator", "")).strip()
    batch_name = str(payload.get("batch_name", "default")).strip() or "default"
    export_file = str(payload.get("export_file", "sync_bundle.json")).strip() or "sync_bundle.json"

    if not tenant or not operator:
        return None

    session = ExportSession(
        workspace=Path("/srv/field_sync"),
        tenant=tenant,
        operator=operator,
        batch_name=batch_name,
        export_file=export_file,
    )
    ensure_workspace(session.workspace)
    return session


def prepare_field_export(request_text: str) -> Dict[str, Any]:
    payload = parse_request(request_text)
    session = build_session(payload)
    if session is None:
        return {"error": "missing tenant or operator"}

    region = str(payload.get("region", "")).strip()
    status = str(payload.get("status", "queued")).strip() or "queued"
    secret = str(payload.get("secret", "")).strip()
    template_name = str(payload.get("template", "agent_note.txt")).strip()
    limit = normalize_limit(payload.get("limit"))

    template = load_template(session.workspace, template_name)
    database_path = session.workspace / "state" / "field_sync.sqlite3"

    with open_database(database_path) as connection:
        session.jobs = fetch_jobs(connection, session.tenant, region, status, limit)
        if not session.jobs:
            return {
                "tenant": session.tenant,
                "batch_name": session.batch_name,
                "written": False,
                "updated": 0,
            }

        export_body = render_export_body(session.jobs, session.operator, template)
        protected = protect_payload(export_body, secret)

        write_checkpoint(session.checkpoint_path, session.jobs)
        write_export_file(session.export_path, protected)

        updated = update_job_state(connection, session.jobs, "prepared")

    return {
        "tenant": session.tenant,
        "batch_name": session.batch_name,
        "file": str(session.export_path),
        "checkpoint": str(session.checkpoint_path),
        "jobs": len(session.jobs),
        "updated": updated,
    }