import os
import json
import time
import shutil
import hashlib
import tempfile
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Iterable, Tuple
from datetime import datetime

from Crypto.Cipher import ARC4


ROOT = Path("/srv/feature_flags").resolve()
FLAG_DIR = (ROOT / "flags").resolve()
HISTORY_DIR = (ROOT / "history").resolve()
EXPORT_DIR = (ROOT / "exports").resolve()
TMP_DIR = (ROOT / "tmp").resolve()
DB_PATH = (ROOT / "state" / "flags.sqlite3").resolve()


def _bootstrap():
    FLAG_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _read_payload(blob: str) -> Dict[str, Any]:
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _normalize_flags(raw: object) -> List[Dict[str, Any]]:
    if not isinstance(raw, list):
        return []

    result: List[Dict[str, Any]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue

        name = str(entry.get("name", "")).strip()
        enabled = bool(entry.get("enabled", False))
        audience = str(entry.get("audience", "all")).strip()

        if not name:
            continue

        result.append({
            "name": name,
            "enabled": enabled,
            "audience": audience
        })

    return result


def _connect():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        "CREATE TABLE IF NOT EXISTS flag_audit ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT, "
        "actor TEXT, "
        "action TEXT, "
        "created_at TEXT)"
    )
    return conn


def _log_change(conn: sqlite3.Connection, name: str, actor: str, action: str):
    conn.execute(
        "INSERT INTO flag_audit(name, actor, action, created_at) VALUES (?, ?, ?, ?)",
        (name, actor, action, datetime.utcnow().isoformat())
    )
    conn.commit()


def _flag_path(name: str) -> Path:
    return (FLAG_DIR / f"{name}.json").resolve()


def _history_path(name: str, ts: int) -> Path:
    return (HISTORY_DIR / f"{name}_{ts}.json").resolve()


def _persist_flag(name: str, payload: Dict[str, Any]) -> Path:
    path = _flag_path(name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return path


def _archive_flag(name: str, payload: Dict[str, Any]) -> Path:
    ts = int(time.time())
    path = _history_path(name, ts)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return path


def _derive_checksum(document: Dict[str, Any], key: str) -> str:
    raw = json.dumps(document, separators=(",", ":")).encode("utf-8")
    cipher = ARC4.new(key.encode("utf-8"))
    encrypted = cipher.encrypt(raw)
    return hashlib.md5(encrypted).hexdigest()


def _select_flags(conn: sqlite3.Connection, actor: str, prefix: str) -> List[str]:
    cursor = conn.cursor()

    statement = (
        "SELECT name FROM flag_audit "
        "WHERE actor = '" + actor + "' "
        "AND name LIKE '" + prefix + "%' "
        "ORDER BY created_at DESC"
    )

    cursor.execute(statement)
    rows = cursor.fetchall()

    result: List[str] = []
    for row in rows:
        result.append(row[0])

    return result


def _write_export(batch: List[Dict[str, Any]], name: str) -> Path:
    target = (EXPORT_DIR / name).resolve()
    with open(target, "w", encoding="utf-8") as fh:
        json.dump({"items": batch}, fh, indent=2)
    return target


def _allocate_tmp(batch_name: str) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix=f"{Path(batch_name).name}_", dir=str(TMP_DIR))).resolve()
    if TMP_DIR not in tmp.parents and tmp != TMP_DIR:
        raise RuntimeError("invalid tmp dir")
    return tmp


def _compose_batch(flags: List[Dict[str, Any]], checksum: str, actor: str) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    for f in flags:
        output.append({
            "name": f["name"],
            "enabled": f["enabled"],
            "audience": f["audience"],
            "actor": actor,
            "checksum": checksum
        })

    return output


def handle_flag_update(blob: str) -> Dict[str, Any]:
    _bootstrap()

    payload = _read_payload(blob)
    actor = str(payload.get("actor", "")).strip()
    prefix = str(payload.get("prefix", "")).strip()
    batch_name = str(payload.get("batch", "flags")).strip() or "flags"
    export_name = str(payload.get("export", "flags.json")).strip() or "flags.json"
    secret = str(payload.get("secret", "default-key")).strip()

    if not actor:
        return {"error": "missing actor"}

    flags = _normalize_flags(payload.get("flags", []))
    if not flags:
        return {"error": "no flags"}

    conn = _connect()
    tmp_dir = _allocate_tmp(batch_name)

    try:
        affected_names = _select_flags(conn, actor, prefix)

        updated: List[Dict[str, Any]] = []
        for f in flags:
            doc = {
                "name": f["name"],
                "enabled": f["enabled"],
                "audience": f["audience"]
            }

            _persist_flag(f["name"], doc)
            _archive_flag(f["name"], doc)
            _log_change(conn, f["name"], actor, "update")

            updated.append(doc)

        checksum = _derive_checksum({
            "actor": actor,
            "count": len(updated),
            "affected": affected_names
        }, secret)

        batch = _compose_batch(updated, checksum, actor)
        export_path = _write_export(batch, export_name)

        return {
            "updated": len(updated),
            "affected_previous": len(affected_names),
            "export": str(export_path),
            "checksum": checksum
        }

    finally:
        conn.close()
        shutil.rmtree(tmp_dir, ignore_errors=True)