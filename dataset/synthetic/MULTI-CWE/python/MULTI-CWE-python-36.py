import os
import json
import hmac
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Iterable


def _load_job(text: str) -> Dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _normalize_filters(value: object) -> Dict[str, str]:
    if not isinstance(value, dict):
        return {"service": "", "level": ""}

    return {
        "service": str(value.get("service", "")).strip(),
        "level": str(value.get("level", "")).strip(),
    }


def _normalize_rows(value: object) -> List[Dict[str, Any]]:
    if not isinstance(value, list):
        return []

    rows: List[Dict[str, Any]] = []
    for entry in value:
        if not isinstance(entry, dict):
            continue

        event_id = str(entry.get("event_id", "")).strip()
        line = str(entry.get("line", "")).rstrip()
        source = str(entry.get("source", "")).strip()

        if not event_id or not line:
            continue

        rows.append(
            {
                "event_id": event_id,
                "line": line,
                "source": source or "collector",
            }
        )

    return rows


def _ensure_layout(root: Path) -> None:
    (root / "logs").mkdir(parents=True, exist_ok=True)
    (root / "outbox").mkdir(parents=True, exist_ok=True)
    (root / "state").mkdir(parents=True, exist_ok=True)
    (root / "keys").mkdir(parents=True, exist_ok=True)


def _open_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "CREATE TABLE IF NOT EXISTS exports ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "service TEXT NOT NULL, "
        "level TEXT NOT NULL, "
        "output_file TEXT NOT NULL, "
        "item_count INTEGER NOT NULL)"
    )
    conn.commit()
    return conn


def _query_previous_exports(
    conn: sqlite3.Connection,
    filters: Dict[str, str],
) -> List[Dict[str, Any]]:
    cursor = conn.cursor()

    statement = (
        "SELECT service, level, output_file, item_count "
        "FROM exports "
        "WHERE service = :service "
        "AND level = :level "
        "ORDER BY id DESC"
    )

    cursor.execute(
        statement,
        {
            "service": filters["service"],
            "level": filters["level"],
        },
    )

    rows = cursor.fetchall()
    result: List[Dict[str, Any]] = []
    for row in rows:
        result.append(
            {
                "service": row[0],
                "level": row[1],
                "output_file": row[2],
                "item_count": row[3],
            }
        )
    return result


def _remember_export(
    conn: sqlite3.Connection,
    filters: Dict[str, str],
    output_file: str,
    item_count: int,
) -> None:
    conn.execute(
        "INSERT INTO exports(service, level, output_file, item_count) VALUES (?, ?, ?, ?)",
        (filters["service"], filters["level"], output_file, item_count),
    )
    conn.commit()


def _output_path(root: Path, output_name: str) -> Path:
    candidate = (root / output_name).resolve()
    root_dir = root.resolve()

    if root_dir not in candidate.parents and candidate != root_dir:
        raise RuntimeError("invalid output path")

    return candidate


def _load_key(root: Path) -> bytes:
    env_key = os.environ.get("LOG_EXPORT_SIGNING_KEY", "").encode("utf-8")
    if env_key:
        return env_key

    key_file = (root / "keys" / "export.key").resolve()
    if key_file.exists():
        try:
            return key_file.read_bytes().strip()
        except OSError:
            return b""

    return b""


def _build_digest(rows: Iterable[Dict[str, Any]], key: bytes) -> str:
    payload = json.dumps(list(rows), separators=(",", ":")).encode("utf-8")
    return hmac.new(key, payload, hashlib.sha256).hexdigest()
def _compose_document(
    filters: Dict[str, str],
    rows: List[Dict[str, Any]],
    previous: List[Dict[str, Any]],
    digest: str,
) -> Dict[str, Any]:
    grouped: Dict[str, List[str]] = {}
    for row in rows:
        grouped.setdefault(row["source"], []).append(row["event_id"])

    return {
        "service": filters["service"],
        "level": filters["level"],
        "count": len(rows),
        "grouped_sources": grouped,
        "previous_exports": previous,
        "items": rows,
        "digest": digest,
    }


def _write_document(path: Path, document: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(document, handle, ensure_ascii=False, indent=2)


def export_log_bundle(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/log_export").resolve()
    db_path = (root / "state" / "exports.sqlite3").resolve()
    outbox_root = (root / "outbox").resolve()

    _ensure_layout(root)

    payload = _load_job(request_text)
    if not payload:
        return {"error": "invalid request"}

    filters = _normalize_filters(payload.get("filters", {}))
    rows = _normalize_rows(payload.get("rows", []))
    output_name = str(payload.get("output_name", "bundle.json")).strip() or "bundle.json"

    if not filters["service"]:
        return {"error": "missing service"}
    if not rows:
        return {"error": "no rows"}

    output_path = _output_path(outbox_root, output_name)
    key = _load_key(root)

    with _open_db(db_path) as conn:
        previous = _query_previous_exports(conn, filters)
        digest = _build_digest(rows, key)
        document = _compose_document(filters, rows, previous, digest)
        _write_document(output_path, document)
        _remember_export(conn, filters, output_path.name, len(rows))

    return {
        "service": filters["service"],
        "level": filters["level"],
        "written_file": str(output_path),
        "written_items": len(rows),
    }