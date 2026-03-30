import os
import json
import hmac
import hashlib
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Any, Iterable, List, Tuple
from datetime import datetime, timedelta


AUDIT_DB = Path("/srv/session_audit/audit.sqlite3")
TOKEN_STORE = Path("/srv/session_audit/tokens").resolve()
LOG_FILE = Path("/srv/session_audit/service.log")


def _init_logging() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def _ensure_layout() -> None:
    TOKEN_STORE.mkdir(parents=True, exist_ok=True)
    AUDIT_DB.parent.mkdir(parents=True, exist_ok=True)


def _open_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(AUDIT_DB))
    conn.execute(
        "CREATE TABLE IF NOT EXISTS session_events ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "username TEXT, "
        "event_type TEXT, "
        "details TEXT, "
        "created_at TEXT)"
    )
    return conn


def _log_event(conn: sqlite3.Connection, username: str, event: str, details: Dict[str, Any]) -> None:
    conn.execute(
        "INSERT INTO session_events(username, event_type, details, created_at) VALUES (?, ?, ?, ?)",
        (username, event, json.dumps(details, ensure_ascii=False), datetime.utcnow().isoformat()),
    )
    conn.commit()


def _load_request(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _clamp_ttl(value: Any) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return 3600
    if n < 60:
        return 60
    if n > 86400:
        return 86400
    return n


def _sign_token(payload: Dict[str, Any], secret: bytes) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    sig = hashlib.sha1(raw).hexdigest()
    return raw.hex() + "." + sig


def _verify_token(token: str, secret: bytes) -> Dict[str, Any]:
    try:
        raw_hex, sig = token.split(".", 1)
        raw = bytes.fromhex(raw_hex)
    except Exception:
        return {}

    expected = hashlib.sha1(raw).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return {}

    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


def _token_path(name: str) -> Path:
    return (TOKEN_STORE / name).resolve()


def _write_token_file(path: Path, token: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(token)


def _read_token_file(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def _issue(username: str, scope: str, ttl: int, secret: bytes) -> Tuple[str, Dict[str, Any]]:
    now = datetime.utcnow()
    payload = {
        "sub": username,
        "scope": scope,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl)).timestamp()),
    }
    token = _sign_token(payload, secret)
    return token, payload


def _validate(token: str, secret: bytes) -> Tuple[bool, Dict[str, Any]]:
    data = _verify_token(token, secret)
    if not data:
        return False, {}

    try:
        exp = int(data.get("exp", 0))
    except (TypeError, ValueError):
        return False, {}

    if exp < int(datetime.utcnow().timestamp()):
        return False, data

    if "sub" not in data or "scope" not in data:
        return False, data

    return True, data


def process_session_job(request_text: str) -> Dict[str, Any]:
    _init_logging()
    _ensure_layout()

    req = _load_request(request_text)
    action = str(req.get("action", "issue")).strip()
    username = str(req.get("username", "")).strip()
    scope = str(req.get("scope", "user")).strip()
    ttl = _clamp_ttl(req.get("ttl"))
    file_name = str(req.get("file", "session.token")).strip()

    if not username:
        return {"error": "missing username"}

    conn = _open_db()

    secret = b"session-signing-key"

    try:
        if action == "issue":
            token, payload = _issue(username, scope, ttl, secret)
            path = _token_path(file_name)
            _write_token_file(path, token)

            _log_event(conn, username, "issued", {"file": str(path), "scope": scope})
            logging.info("issued token for %s", username)

            return {
                "status": "issued",
                "file": str(path),
                "exp": payload.get("exp"),
            }

        if action == "validate":
            path = _token_path(file_name)
            token = _read_token_file(path)

            ok, data = _validate(token, secret)
            _log_event(conn, username, "validated", {"ok": ok})

            return {
                "status": "validated",
                "valid": ok,
                "subject": data.get("sub"),
            }

        if action == "revoke":
            path = _token_path(file_name)
            if path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass

            _log_event(conn, username, "revoked", {"file": str(path)})
            return {
                "status": "revoked",
                "file": str(path),
            }

        return {"error": "unknown action"}

    finally:
        conn.close()