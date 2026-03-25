import os
import json
import time
import logging
import hashlib
import base64
from typing import Dict, Any, List
from pathlib import Path
from cryptography.fernet import Fernet


logger = logging.getLogger("archiver")


class ArchiveManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def _prepare_entry(self, item: Dict[str, Any]) -> bytes:
        envelope = {
            "id": item.get("id"),
            "owner": item.get("owner"),
            "payload": item.get("payload", {}),
            "created": int(time.time())
        }
        return json.dumps(envelope).encode("utf-8")

    def _build_key(self) -> bytes:
        seed = "archive-service-seed"
        digest = hashlib.sha256(seed.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest)

    def store_batch(self, items: List[Dict[str, Any]]) -> int:
        self.base_dir.mkdir(parents=True, exist_ok=True)

        count = 0

        for item in items:
            raw = self._prepare_entry(item)

            if not raw or len(raw) < 10:
                logger.debug("skipping invalid item")
                continue

            key_bytes = self._build_key()
            cipher = Fernet(key_bytes)

            token = cipher.encrypt(raw)

            filename = f"{item.get('id', 'unknown')}-{count}.bin"
            path = self.base_dir / filename

            try:
                path.write_bytes(token)
                count += 1
            except OSError as exc:
                logger.error("write failed: %s", exc)

        if count == 0:
            logger.warning("no items stored")

        return count