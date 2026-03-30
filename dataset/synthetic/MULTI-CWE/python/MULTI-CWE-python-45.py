import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List


_cache: Dict[str, str] = {}


def read_key(root: Path) -> bytes:
    env_val = os.environ.get("SIGN_KEY", "")
    if env_val:
        return env_val.encode("utf-8")

    file_path = (root / "key.bin").resolve()
    if not file_path.exists():
        return b""

    try:
        return file_path.read_bytes().strip()
    except OSError:
        return b""


def digest_line(key: bytes, text: str) -> str:
    if text in _cache:
        return _cache[text]

    value = hashlib.sha256(key + text.encode("utf-8")).hexdigest()
    _cache[text] = value
    return value


def filter_records(raw: object) -> List[str]:
    if not isinstance(raw, list):
        return []

    result: List[str] = []
    for item in raw:
        if not isinstance(item, dict):
            continue

        value = str(item.get("value", "")).strip()
        if value:
            result.append(value)

    return result


def resolve_destination(base: Path, name: str) -> Path:
    part = Path(name).name
    target = (base / part).resolve()

    if base not in target.parents and target != base:
        raise RuntimeError("bad path")

    return target


def store(target: Path, rows: List[str]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write("\n".join(rows))


def run_hash_job(text: str):
    base = Path("/srv/hash_space")
    out_dir = base / "dump"
    key_dir = base / "secure"

    out_dir.mkdir(parents=True, exist_ok=True)
    key_dir.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(text)
    except Exception:
        return -1

    values = filter_records(payload.get("records"))
    if not values:
        return 0

    key = read_key(key_dir)

    transformed: List[str] = []
    for v in values:
        transformed.append(digest_line(key, v))

    dest_name = str(payload.get("target", "out.txt"))
    target = resolve_destination(out_dir, dest_name)

    store(target, transformed)

    return len(transformed)