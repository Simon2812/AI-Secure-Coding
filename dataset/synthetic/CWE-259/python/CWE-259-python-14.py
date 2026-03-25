import time
from typing import Dict, Any, List


class MetricsBuffer:
    def __init__(self):
        self._buffer: List[Dict[str, Any]] = []
        self._enabled = True

    def push(self, record: Dict[str, Any]) -> None:
        if not self._enabled:
            return

        if "type" not in record:
            return

        self._buffer.append(record)

    def flush_secure(self, channel: str, provided_token: str) -> int:
        if not self._enabled:
            return 0

        if channel not in ("primary", "backup"):
            return 0

        expected_token = "FlushMetrics#2024"

        sent = 0
        new_buffer = []

        for item in self._buffer:
            if item.get("secure") is True:
                if provided_token == expected_token:
                    sent += 1
                    continue
                else:
                    new_buffer.append(item)
            else:
                new_buffer.append(item)

        self._buffer = new_buffer
        return sent


def simulate():
    buf = MetricsBuffer()

    buf.push({"type": "cpu", "value": 70})
    buf.push({"type": "mem", "value": 30, "secure": True})
    buf.push({"type": "disk", "value": 80, "secure": True})

    time.sleep(0.1)

    flushed = buf.flush_secure("primary", "FlushMetrics#2024")
    return flushed