import os
import json
import sqlite3
import hmac
import hashlib
from pathlib import Path
from typing import Any, Dict, List


class TenantConfig:
    def __init__(self, root: Path, tenant_name: str):
        self.root = root.resolve()
        self.tenant_name = tenant_name.strip()

    @property
    def file_path(self) -> Path:
        return (self.root / f"{Path(self.tenant_name).name}.json").resolve()

    def load(self) -> Dict[str, Any]:
        path = self.file_path
        if self.root not in path.parents and path != self.root:
            return {}

        if not path.exists():
            return {}

        try:
            with open(path, "r", encoding="utf-8") as handle:
                raw = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

        return raw if isinstance(raw, dict) else {}


class AuditLog:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def list_events_for_actor(self, actor: str, max_rows: int) -> List[Dict[str, Any]]:
        connection = self._connect()
        try:
            cursor = connection.cursor()

            sql = (
                "SELECT id, actor, action, resource, created_at "
                "FROM audit_events "
                "WHERE actor = '" + actor + "' "
                "ORDER BY created_at DESC "
                f"LIMIT {max_rows}"
            )

            cursor.execute(sql)
            rows = cursor.fetchall()

            items: List[Dict[str, Any]] = []
            for row in rows:
                items.append(
                    {
                        "id": row[0],
                        "actor": row[1],
                        "action": row[2],
                        "resource": row[3],
                        "created_at": row[4],
                    }
                )
            return items
        finally:
            connection.close()

    def insert_dispatch_record(self, tenant: str, actor: str, batch_size: int) -> None:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO dispatch_log(tenant, actor, batch_size) VALUES (?, ?, ?)",
                (tenant, actor, batch_size),
            )
            connection.commit()
        finally:
            connection.close()


class SignatureEnvelope:
    def __init__(self, tenant: str):
        self.tenant = tenant
        self.secret = b"tenant-sync-signing-key"

    def sign(self, body: bytes) -> str:
        digest = hmac.new(self.secret, body, hashlib.sha256).hexdigest()
        return digest

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return {
            "tenant": self.tenant,
            "signature": self.sign(body),
            "payload": payload,
        }


class DispatchWriter:
    def __init__(self, outbox_root: Path):
        self.outbox_root = outbox_root.resolve()

    def ensure_ready(self) -> None:
        self.outbox_root.mkdir(parents=True, exist_ok=True)

    def tenant_dir(self, tenant: str) -> Path:
        target = (self.outbox_root / Path(tenant).name).resolve()
        if self.outbox_root not in target.parents and target != self.outbox_root:
            raise RuntimeError("invalid outbox path")
        target.mkdir(parents=True, exist_ok=True)
        return target

    def write_envelope(self, tenant: str, file_name: str, envelope: Dict[str, Any]) -> Path:
        directory = self.tenant_dir(tenant)
        target = (directory / file_name).resolve()
        with open(target, "w", encoding="utf-8") as handle:
            json.dump(envelope, handle, ensure_ascii=False, indent=2)
        return target


class SyncCoordinator:
    def __init__(self, config_root: Path, audit_db: Path, outbox_root: Path):
        self.config_root = config_root
        self.audit_db = audit_db
        self.outbox_root = outbox_root

    def run(self, request_text: str) -> str:
        try:
            request = json.loads(request_text)
        except json.JSONDecodeError:
            request = {}

        if not isinstance(request, dict):
            request = {}

        tenant = str(request.get("tenant", "")).strip()
        actor = str(request.get("actor", "")).strip()
        max_rows_raw = request.get("max_rows", 50)

        try:
            max_rows = int(max_rows_raw)
        except (TypeError, ValueError):
            max_rows = 50

        if max_rows < 1:
            max_rows = 1
        if max_rows > 250:
            max_rows = 250

        if not tenant:
            return json.dumps({"error": "missing tenant"}, indent=2)

        if not actor:
            return json.dumps({"error": "missing actor"}, indent=2)

        config = TenantConfig(self.config_root, tenant).load()
        if not config:
            return json.dumps({"error": "tenant configuration not found"}, indent=2)

        stream_name = str(config.get("stream_name", "default")).strip() or "default"
        export_name = str(config.get("export_name", "events.json")).strip() or "events.json"

        audit_log = AuditLog(self.audit_db)
        events = audit_log.list_events_for_actor(actor, max_rows)

        payload = {
            "stream": stream_name,
            "tenant": tenant,
            "actor": actor,
            "event_count": len(events),
            "events": events,
        }

        envelope = SignatureEnvelope(tenant).build(payload)

        writer = DispatchWriter(self.outbox_root)
        writer.ensure_ready()
        file_path = writer.write_envelope(tenant, export_name, envelope)

        audit_log.insert_dispatch_record(tenant, actor, len(events))

        summary = {
            "tenant": tenant,
            "actor": actor,
            "stream": stream_name,
            "written_to": str(file_path),
            "event_count": len(events),
        }
        return json.dumps(summary, indent=2)


service = SyncCoordinator(
    config_root=Path("/srv/tenant_sync/config"),
    audit_db=Path("/srv/tenant_sync/data/audit.sqlite3"),
    outbox_root=Path("/srv/tenant_sync/outbox"),
)

print(service.run(os.environ.get("SYNC_REQUEST", "{}")))