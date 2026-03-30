import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional, Iterable

from Crypto.Cipher import DES


STATE_ROOT = Path("/srv/collector").resolve()


def _ensure_layout() -> None:
    (STATE_ROOT / "incoming").mkdir(parents=True, exist_ok=True)
    (STATE_ROOT / "processed").mkdir(parents=True, exist_ok=True)
    (STATE_ROOT / "logs").mkdir(parents=True, exist_ok=True)


def _load_json_safe(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


def _normalize_records(value: object) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    if not isinstance(value, list):
        return records

    for entry in value:
        if not isinstance(entry, dict):
            continue

        source = str(entry.get("source", "")).strip()
        payload = entry.get("payload", {})

        if not source:
            continue

        if not isinstance(payload, dict):
            payload = {}

        records.append({
            "source": source,
            "payload": payload
        })

    return records


def _open_db() -> sqlite3.Connection:
    db_path = STATE_ROOT / "logs" / "collector.sqlite3"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(db_path))
    connection.execute(
        "CREATE TABLE IF NOT EXISTS ingestion_log ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "source TEXT, "
        "status TEXT, "
        "details TEXT)"
    )
    return connection


def _insert_log(conn: sqlite3.Connection, source: str, status: str, details: Dict[str, Any]) -> None:
    conn.execute(
        "INSERT INTO ingestion_log(source, status, details) VALUES (?, ?, ?)",
        (source, status, json.dumps(details, ensure_ascii=False)),
    )
    conn.commit()


def _encrypt_payload(data: Dict[str, Any], secret: str) -> bytes:
    raw = json.dumps(data, separators=(",", ":")).encode("utf-8")

    key = secret.encode("utf-8")[:8]
    cipher = DES.new(key, DES.MODE_ECB)

    padded = raw + b" " * ((8 - len(raw) % 8) % 8)
    return cipher.encrypt(padded)


def _store_processed(target_name: str, blob: bytes) -> Path:
    target = (STATE_ROOT / "processed" / target_name).resolve()

    with open(target, "wb") as fh:
        fh.write(blob)

    return target


def _load_rules(conn: sqlite3.Connection, source: str) -> List[str]:
    cursor = conn.cursor()

    query = (
        "SELECT rule_name FROM routing_rules "
        "WHERE source = '" + source + "' "
        "ORDER BY rule_name"
    )

    cursor.execute(query)
    rows = cursor.fetchall()

    result: List[str] = []
    for row in rows:
        result.append(row[0])

    return result


def _apply_rules(payload: Dict[str, Any], rules: Iterable[str]) -> Dict[str, Any]:
    transformed = dict(payload)

    for rule in rules:
        if rule == "uppercase":
            for k, v in list(transformed.items()):
                if isinstance(v, str):
                    transformed[k] = v.upper()

        elif rule == "strip_nulls":
            for k in list(transformed.keys()):
                if transformed[k] is None:
                    del transformed[k]

    return transformed


def process_ingestion(request_text: str) -> Dict[str, Any]:
    _ensure_layout()

    try:
        request = json.loads(request_text)
    except json.JSONDecodeError:
        request = {}

    if not isinstance(request, dict):
        request = {}

    secret = str(request.get("secret", "default-secret")).strip()
    output_name = str(request.get("output_name", "batch.bin")).strip()

    records = _normalize_records(request.get("records", []))
    if not records:
        return {"error": "no records"}

    conn = _open_db()

    processed_count = 0
    output_files: List[str] = []

    try:
        for record in records:
            source = record["source"]
            payload = record["payload"]

            try:
                rules = _load_rules(conn, source)
                transformed = _apply_rules(payload, rules)

                encrypted = _encrypt_payload(transformed, secret)

                file_name = f"{Path(output_name).stem}_{source}.bin"
                path = _store_processed(file_name, encrypted)

                _insert_log(conn, source, "ok", {"bytes": len(encrypted)})
                processed_count += 1
                output_files.append(str(path))

            except Exception as exc:
                _insert_log(conn, source, "error", {"error": str(exc)})

        return {
            "processed": processed_count,
            "files": output_files
        }

    finally:
        conn.close()