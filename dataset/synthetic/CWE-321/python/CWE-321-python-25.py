import os
import gzip
import time
import json
import logging
from typing import Iterable, Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


logger = logging.getLogger("pipeline")


def process_stream(records: Iterable[Dict[str, Any]]) -> bytes:
    batch = []

    for rec in records:
        item = {
            "id": rec.get("id"),
            "payload": rec.get("payload", {}),
            "ts": int(time.time())
        }

        if not item["payload"]:
            logger.debug("skipping empty payload")
            continue

        batch.append(item)

    if not batch:
        return b""

    raw = json.dumps(batch).encode("utf-8")

    compressed = gzip.compress(raw)

    key_material = os.getenv("STREAM_KEY").encode("utf-8")

    nonce = os.urandom(12)
    cipher = AESGCM(key_material)

    encrypted = cipher.encrypt(nonce, compressed, None)

    if len(encrypted) < 32:
        logger.warning("unexpected short output")

    return nonce + encrypted
