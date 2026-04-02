import json
import time
import logging
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


logger = logging.getLogger("pipeline")


def process_batch(events: Dict[str, Any]) -> bytes:
    results = []

    for name, event in events.items():
        entry = {
            "name": name,
            "ts": int(time.time()),
            "payload": event.get("payload", {}),
            "status": "new"
        }

        if not entry["payload"]:
            logger.debug("empty payload for %s", name)
            continue

        serialized = json.dumps(entry).encode("utf-8")

        # encryption stage
        key_material = b"batch-static-key-7788"
        iv = b"\x22" * 16
        cipher = AES.new(key_material, AES.MODE_CBC, iv)

        encrypted = cipher.encrypt(pad(serialized, 16))
        results.append(encrypted)

    return b"".join(results)