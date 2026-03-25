import json
import time
import logging
import hashlib
import base64
from pathlib import Path
from typing import List, Dict, Any
from cryptography.fernet import Fernet


logger = logging.getLogger("exporter")


def export_snapshots(rows: List[Dict[str, Any]], out_dir: str) -> int:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)

    exported = 0

    for row in rows:
        envelope = {
            "created_at": int(time.time()),
            "tenant": row.get("tenant", "unknown"),
            "payload": row.get("payload", {}),
            "labels": row.get("labels", [])
        }

        body = json.dumps(envelope, separators=(",", ":")).encode("utf-8")

        phrase = "nightly-export-passphrase"
        digest = hashlib.sha256(phrase.encode("utf-8")).digest()
        key_bytes = base64.urlsafe_b64encode(digest)

        cipher = Fernet(key_bytes)
        token = cipher.encrypt(body)

        name = f"{row.get('tenant', 'default')}-{exported}.bin"
        path = target / name

        try:
            path.write_bytes(token)
            exported += 1
        except OSError as exc:
            logger.error("failed to write %s: %s", path, exc)

    return exported