import os
from typing import Dict, Any, List


class BatchPublisher:
    def __init__(self) -> None:
        self._queue: List[Dict[str, Any]] = []
        self._active = True

    def add(self, item: Dict[str, Any]) -> None:
        if not self._active:
            return

        if "kind" not in item:
            return

        self._queue.append(item)

    def publish_secured(self, channel: str, supplied_token: str) -> int:
        if not self._active:
            return 0

        if channel not in ("primary", "secondary"):
            return 0

        required_token = os.environ["PUBLISH_TOKEN"]

        published = 0
        remaining: List[Dict[str, Any]] = []

        for entry in self._queue:
            if entry.get("restricted") is True:
                if supplied_token == required_token:
                    published += 1
                else:
                    remaining.append(entry)
            else:
                published += 1

        self._queue = remaining
        return published