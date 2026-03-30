import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List


def _read_key(root: Path) -> bytes:
    env_val = os.environ.get("BUNDLE_KEY", "")
    if env_val:
        return env_val.encode("utf-8")

    f = (root / "bundle.key").resolve()
    if not f.exists():
        return b""

    try:
        return f.read_bytes().strip()
    except OSError:
        return b""


def _digest_bytes(key: bytes, blob: bytes) -> str:
    return hashlib.sha256(key + blob).hexdigest()


def _normalize_paths(root: Path, items: List[Dict[str, Any]]) -> List[Path]:
    resolved: List[Path] = []

    for entry in items:
        raw = str(entry.get("name", "")).strip()
        if not raw:
            continue

        part = Path(raw).name
        candidate = (root / part).resolve()

        if root not in candidate.parents and candidate != root:
            continue

        resolved.append(candidate)

    return resolved


def _load_existing(paths: List[Path]) -> List[bytes]:
    chunks: List[bytes] = []

    for p in paths:
        if not p.exists():
            continue

        try:
            chunks.append(p.read_bytes())
        except OSError:
            continue

    return chunks


def _merge(chunks: List[bytes]) -> bytes:
    total = bytearray()
    for c in chunks:
        total.extend(c)
    return bytes(total)


def _emit(root: Path, name: str, payload: bytes) -> Path:
    part = Path(name).name
    out = (root / part).resolve()

    if root not in out.parents and out != root:
        raise RuntimeError("bad path")

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        f.write(payload)

    return out


def run_bundle_job(req: str):
    base = Path("/srv/bundle_engine")
    in_dir = base / "input"
    out_dir = base / "output"
    key_dir = base / "keys"

    in_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    key_dir.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(req)
    except Exception:
        return None

    items = payload.get("files")
    if not isinstance(items, list):
        return None

    targets = _normalize_paths(in_dir, items)
    if not targets:
        return None

    chunks = _load_existing(targets)
    if not chunks:
        return None

    merged = _merge(chunks)

    key = _read_key(key_dir)
    signature = _digest_bytes(key, merged)

    name = str(payload.get("output", "bundle.bin"))
    out_path = _emit(out_dir, name, merged)

    return {
        "size": len(merged),
        "signature": signature,
        "location": str(out_path),
    }