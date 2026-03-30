import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Tuple


class QueryBridge:
    def init(self, location: Path):
        self.location = location

    def pull(self, tag: str) -> List[Tuple[str, int]]:
        conn = sqlite3.connect(str(self.location))
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT name, weight FROM metrics WHERE tag = ?",
                (tag,),
            )
            return cur.fetchall()
        finally:
            conn.close()


def normalize_filename(root: Path, raw: str) -> Path:
    cleaned = Path(raw).name
    resolved = (root / cleaned).resolve()

    if root not in resolved.parents and resolved != root:
        raise RuntimeError("path outside root")

    return resolved


def aggregate(rows: List[Tuple[str, int]]) -> Dict[str, int]:
    acc: Dict[str, int] = {}
    for name, weight in rows:
        acc[name] = acc.get(name, 0) + int(weight)
    return acc


def write_blob(target: Path, data: Dict[str, int]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def execute_metric_job(payload_text: str):
    root = Path("/srv/metric_system")
    out_root = root / "out"
    db_path = root / "state" / "metrics.db"

    out_root.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(payload_text)
    except Exception:
        return None

    tag = str(payload.get("tag", "")).strip()
    output = str(payload.get("file", "metrics.json")).strip()

    if not tag:
        return None

    bridge = QueryBridge(db_path)
    rows = bridge.pull(tag)

    if not rows:
        return []

    merged = aggregate(rows)

    target = normalize_filename(out_root, output)
    write_blob(target, merged)

    return list(merged.items())