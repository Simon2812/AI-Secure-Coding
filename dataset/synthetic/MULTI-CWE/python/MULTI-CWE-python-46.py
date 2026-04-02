import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List


def _open(db: Path):
    return sqlite3.connect(str(db))


def _collect(cur, category: str) -> List[Dict[str, Any]]:
    cur.execute(
        "SELECT code, amount FROM transactions WHERE category = ?",
        (category,),
    )
    rows = cur.fetchall()

    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append({"code": r[0], "amount": float(r[1])})
    return out


def _group(entries: List[Dict[str, Any]]) -> Dict[str, float]:
    acc: Dict[str, float] = {}
    for e in entries:
        acc[e["code"]] = acc.get(e["code"], 0.0) + e["amount"]
    return acc


def _target(root: Path, raw: str) -> Path:
    name = Path(raw).name
    candidate = (root / name).resolve()

    if root not in candidate.parents and candidate != root:
        raise RuntimeError("bad path")

    return candidate


def _dump(p: Path, data: Dict[str, float]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for k, v in data.items():
            f.write(f"{k}:{v}\n")


def execute_rollup(req: str):
    base = Path("/srv/rollup_engine")
    db_file = base / "state" / "tx.db"
    out_dir = base / "exports"

    out_dir.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        data = json.loads(req)
    except Exception:
        return {}

    cat = str(data.get("category", "")).strip()
    name = str(data.get("file", "rollup.txt")).strip()

    if not cat:
        return {}

    conn = _open(db_file)
    try:
        cur = conn.cursor()
        items = _collect(cur, cat)
    finally:
        conn.close()

    if not items:
        return {}

    merged = _group(items)

    dest = _target(out_dir, name)
    _dump(dest, merged)

    return merged