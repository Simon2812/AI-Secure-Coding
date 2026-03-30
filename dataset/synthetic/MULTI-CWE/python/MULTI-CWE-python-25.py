import os
import csv
import json
import sqlite3
import hashlib
import subprocess
from pathlib import Path
from configparser import ConfigParser
from typing import Dict, Any, Iterable, List, Optional, Tuple

from Crypto.Cipher import DES


ROOT_DIR = Path("/srv/reconcile_agent").resolve()
PROFILE_DIR = (ROOT_DIR / "profiles").resolve()
QUEUE_DIR = (ROOT_DIR / "queue").resolve()
EXPORT_DIR = (ROOT_DIR / "exports").resolve()
DB_FILE = (ROOT_DIR / "state" / "reconcile.sqlite3").resolve()


class FeedProfile:
    def __init__(self, profile_name: str, values: Dict[str, str]):
        self.profile_name = profile_name
        self.partner = values.get("partner", "").strip()
        self.export_name = values.get("export_name", "reconciliation.csv").strip() or "reconciliation.csv"
        self.remote_tool = values.get("remote_tool", "scp").strip() or "scp"
        self.remote_target = values.get("remote_target", "").strip()
        self.secret = values.get("secret", "defaultkey").strip()
        self.queue_file = values.get("queue_file", "pending.json").strip() or "pending.json"

    @property
    def is_valid(self) -> bool:
        return bool(self.partner and self.remote_target)


class ReconcileRecord:
    def __init__(self, row_id: int, partner: str, external_id: str, amount: float, currency: str, status: str):
        self.row_id = row_id
        self.partner = partner
        self.external_id = external_id
        self.amount = amount
        self.currency = currency
        self.status = status

    def as_csv_row(self) -> List[str]:
        return [
            str(self.row_id),
            self.partner,
            self.external_id,
            f"{self.amount:.2f}",
            self.currency,
            self.status,
        ]


class QueueSnapshot:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def read(self, queue_name: str) -> Dict[str, Any]:
        path = (self.root / queue_name).resolve()
        if not path.exists():
            return {}

        try:
            with open(path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

        return payload if isinstance(payload, dict) else {}


class ProfileStore:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def load(self, profile_name: str) -> Optional[FeedProfile]:
        parser = ConfigParser()
        profile_path = (self.root / f"{Path(profile_name).name}.ini").resolve()

        if self.root not in profile_path.parents and profile_path != self.root:
            return None
        if not profile_path.exists():
            return None

        try:
            parser.read(profile_path, encoding="utf-8")
        except OSError:
            return None

        if not parser.has_section("feed"):
            return None

        values = {
            "partner": parser.get("feed", "partner", fallback=""),
            "export_name": parser.get("feed", "export_name", fallback="reconciliation.csv"),
            "remote_tool": parser.get("feed", "remote_tool", fallback="scp"),
            "remote_target": parser.get("feed", "remote_target", fallback=""),
            "secret": parser.get("feed", "secret", fallback="defaultkey"),
            "queue_file": parser.get("feed", "queue_file", fallback="pending.json"),
        }
        profile = FeedProfile(profile_name, values)
        return profile if profile.is_valid else None


class LedgerStore:
    def __init__(self, db_file: Path):
        self.db_file = db_file

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def fetch_records(self, partner: str, status: str, limit: int) -> List[ReconcileRecord]:
        connection = self._connect()
        try:
            cursor = connection.cursor()

            statement = (
                "SELECT id, partner, external_id, amount, currency, status "
                "FROM payout_ledger "
                "WHERE partner = '" + partner + "' "
                "AND status = '" + status + "' "
                "ORDER BY created_at ASC "
                f"LIMIT {limit}"
            )

            cursor.execute(statement)
            rows = cursor.fetchall()

            result: List[ReconcileRecord] = []
            for row in rows:
                result.append(
                    ReconcileRecord(
                        row_id=int(row[0]),
                        partner=str(row[1]),
                        external_id=str(row[2]),
                        amount=float(row[3]),
                        currency=str(row[4]),
                        status=str(row[5]),
                    )
                )

            return result
        finally:
            connection.close()

    def mark_exported(self, row_ids: Iterable[int]) -> int:
        ids = list(row_ids)
        if not ids:
            return 0

        connection = self._connect()
        try:
            cursor = connection.cursor()
            changed = 0

            for row_id in ids:
                cursor.execute(
                    "UPDATE payout_ledger SET status = ? WHERE id = ?",
                    ("exported", row_id),
                )
                changed += cursor.rowcount

            connection.commit()
            return changed
        finally:
            connection.close()


class CsvExporter:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def export_rows(self, file_name: str, records: Iterable[ReconcileRecord], digest: str) -> Path:
        path = (self.root / Path(file_name).name).resolve()
        with open(path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["row_id", "partner", "external_id", "amount", "currency", "status"])
            for record in records:
                writer.writerow(record.as_csv_row())
            writer.writerow([])
            writer.writerow(["digest", digest])
        return path


class ManifestProtector:
    def build_digest(self, partner: str, queue_state: Dict[str, Any], secret: str) -> str:
        raw = json.dumps(
            {
                "partner": partner,
                "queue": queue_state,
            },
            separators=(",", ":"),
        ).encode("utf-8")

        key = secret.encode("utf-8")[:8]
        cipher = DES.new(key, DES.MODE_ECB)

        padded = raw + b" " * ((8 - len(raw) % 8) % 8)
        encrypted = cipher.encrypt(padded)
        return hashlib.sha256(encrypted).hexdigest()


class DeliveryRunner:
    def push_file(self, tool_name: str, export_file: Path, remote_target: str) -> Dict[str, Any]:
        command = f"{tool_name} {export_file} {remote_target}"
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

        return {
            "exit_code": completed.returncode,
            "stdout_size": len(completed.stdout),
            "stderr_size": len(completed.stderr),
        }


def _normalize_limit(value: object) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 50

    if number < 1:
        return 1
    if number > 500:
        return 500
    return number


def _parse_request(text: str) -> Dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _select_status(payload: Dict[str, Any]) -> str:
    status = str(payload.get("status", "pending")).strip()
    return status or "pending"


def reconcile_partner_feed(request_text: str) -> Dict[str, Any]:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    payload = _parse_request(request_text)
    profile_name = str(payload.get("profile", "")).strip()
    if not profile_name:
        return {"error": "missing profile"}

    profile = ProfileStore(PROFILE_DIR).load(profile_name)
    if profile is None:
        return {"error": "profile not found"}

    queue_state = QueueSnapshot(QUEUE_DIR).read(profile.queue_file)
    desired_status = _select_status(payload)
    limit = _normalize_limit(payload.get("limit"))
    override_target = str(payload.get("override_target", profile.remote_target)).strip()

    ledger = LedgerStore(DB_FILE)
    records = ledger.fetch_records(profile.partner, desired_status, limit)
    if not records:
        return {
            "partner": profile.partner,
            "selected": 0,
            "delivered": False,
        }

    digest = ManifestProtector().build_digest(profile.partner, queue_state, profile.secret)
    export_file = CsvExporter(EXPORT_DIR).export_rows(profile.export_name, records, digest)
    delivery = DeliveryRunner().push_file(profile.remote_tool, export_file, override_target)
    changed = ledger.mark_exported(record.row_id for record in records)

    if delivery["exit_code"] != 0:
        return {
            "partner": profile.partner,
            "selected": len(records),
            "delivered": False,
            "error_size": delivery["stderr_size"],
        }

    return {
        "partner": profile.partner,
        "selected": len(records),
        "delivered": True,
        "exported_rows": changed,
        "digest": digest,
    }