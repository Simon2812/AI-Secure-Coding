import os
import json
import sqlite3
import hashlib
from collections import deque
from pathlib import Path
from typing import Dict, Any, Deque, Iterable, List, Optional, Tuple


class WindowBuffer:
    def init(self, limit: int):
        self.limit = limit
        self._rows: Deque[Dict[str, Any]] = deque(maxlen=limit)

    def append(self, row: Dict[str, Any]) -> None:
        self._rows.append(row)

    def snapshot(self) -> List[Dict[str, Any]]:
        return list(self._rows)


class RecordCursor:
    def init(self, db_file: Path):
        self.db_file = db_file

    def open(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def scan(self, connection: sqlite3.Connection, stream_name: str, state: str, limit: int) -> Iterable[Tuple[str, str, int]]:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT record_id, payload, size_hint "
            "FROM stream_records "
            "WHERE stream_name = ? AND state = ? "
            "ORDER BY created_at DESC "
            "LIMIT ?",
            (stream_name, state, limit),
        )
        for row in cursor.fetchall():
            yield str(row[0]), str(row[1]), int(row[2])


class KeyRing:
    def init(self, root: Path):
        self.root = root.resolve()

    def current(self, channel: str) -> bytes:
        env_name = f"STREAM_KEY_{channel.upper()}"
        env_value = os.environ.get(env_name, "")
        if env_value:
            return env_value.encode("utf-8")

        file_name = f"{Path(channel).name}.key"
        candidate = (self.root / file_name).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            return b""

        if not candidate.exists():
            return b""

        try:
            return candidate.read_bytes().strip()
        except OSError:
            return b""


class DigestAccumulator:
    def init(self, key: bytes):
        self.key = key
        self._hasher = hashlib.sha256()
        if key:
            self._hasher.update(key)

    def update(self, record_id: str, payload: str, size_hint: int) -> None:
        encoded = json.dumps(
            {
                "record_id": record_id,
                "payload": payload,
                "size_hint": size_hint,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        self._hasher.update(encoded)

    def value(self) -> str:
        return self._hasher.hexdigest()


class OutputPort:
    def init(self, root: Path):
        self.root = root.resolve()

    def resolve(self, name: str) -> Path:
        part = Path(name).name
        candidate = (self.root / part).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            raise RuntimeError("invalid output path")
        return candidate

    def store(self, target: Path, document: Dict[str, Any]) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)


def _parse_request(text: str) -> Optional[Dict[str, Any]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _bounded_limit(value: object) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 25
    if number < 1:
        return 1
    if number > 200:
        return 200
    return number


def _shrink_payload(payload: str, max_chars: int) -> str:
    if len(payload) <= max_chars:
        return payload
    return payload[:max_chars]


def _compose_rows(rows: Iterable[Tuple[str, str, int]], digest: DigestAccumulator, window: WindowBuffer) -> int:
    count = 0
    for record_id, payload, size_hint in rows:
        digest.update(record_id, payload, size_hint)
        window.append(
            {
                "record_id": record_id,
                "payload_preview": _shrink_payload(payload, 60),
                "size_hint": size_hint,
            }
        )
        count += 1
    return count


def run_window_export(request_text: str):
    base = Path("/srv/window_export").resolve()
    out_root = (base / "outbox").resolve()
    key_root = (base / "keys").resolve()
    db_file = (base / "state" / "streams.sqlite3").resolve()

    out_root.mkdir(parents=True, exist_ok=True)
    key_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    payload = _parse_request(request_text)
    if payload is None:
        return None

    stream_name = str(payload.get("stream", "")).strip()
    state = str(payload.get("state", "ready")).strip() or "ready"
    channel = str(payload.get("channel", "default")).strip() or "default"
    output_name = str(payload.get("output", "window.json")).strip() or "window.json"

    if not stream_name:
        return None

    limit = _bounded_limit(payload.get("limit"))
    reader = RecordCursor(db_file)
    key = KeyRing(key_root).current(channel)
    digest = DigestAccumulator(key)
    window = WindowBuffer(limit=min(limit, 10))

    connection = reader.open()
    try:
        rows = reader.scan(connection, stream_name, state, limit)
        processed = _compose_rows(rows, digest, window)
    finally:
        connection.close()

    if processed == 0:
        return ()

    document = {
        "stream": stream_name,
        "state": state,
        "processed": processed,
        "window": window.snapshot(),
        "digest": digest.value(),
    }

    target = OutputPort(out_root).resolve(output_name)
    OutputPort(out_root).store(target, document)

    return target.name, processed