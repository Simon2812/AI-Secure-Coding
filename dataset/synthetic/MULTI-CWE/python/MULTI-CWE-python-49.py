import json
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional


class Snapshot:
    def init(self):
        self._data: Dict[str, int] = {}

    def add(self, key: str, value: int) -> None:
        self._data[key] = self._data.get(key, 0) + value

    def export(self) -> Dict[str, int]:
        return dict(self._data)


class DbReader:
    def init(self, db: Path):
        self.db = db

    def fetch(self, scope: str):
        conn = sqlite3.connect(str(self.db))
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT metric, amount FROM usage WHERE scope = ?",
                (scope,),
            )
            for row in cur.fetchall():
                yield row[0], int(row[1])
        finally:
            conn.close()


class HashSink:
    def init(self):
        self._h = hashlib.sha256()

    def absorb(self, key: str, value: int) -> None:
        blob = f"{key}:{value}".encode("utf-8")
        self._h.update(blob)

    def finish(self) -> str:
        return self._h.hexdigest()


class PathBox:
    def init(self, root: Path):
        self.root = root.resolve()

    def pick(self, raw: str) -> Path:
        part = Path(raw).name
        p = (self.root / part).resolve()
        if self.root not in p.parents and p != self.root:
            raise RuntimeError("invalid path")
        return p


def _parse(text: str) -> Optional[Dict[str, Any]]:
    try:
        obj = json.loads(text)
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def run_usage_snapshot(text: str):
    base = Path("/srv/usage_engine")
    db_file = base / "state" / "usage.db"
    out_root = base / "snapshots"

    out_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    payload = _parse(text)
    if payload is None:
        return False

    scope = str(payload.get("scope", "")).strip()
    name = str(payload.get("file", "snapshot.json")).strip()

    if not scope:
        return False

    reader = DbReader(db_file)
    snap = Snapshot()
    sink = HashSink()

    for metric, amount in reader.fetch(scope):
        snap.add(metric, amount)
        sink.absorb(metric, amount)

    data = snap.export()
    if not data:
        return False

    target = PathBox(out_root).pick(name)
    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "entries": data,
                "fingerprint": sink.finish(),
            },
            handle,
            indent=2,
        )

    return True