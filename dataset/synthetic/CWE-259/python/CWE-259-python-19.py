from typing import List, Dict, Any


def load_secret(path: str) -> str:
    with open(path, "r") as f:
        return f.read().strip()


class SyncAgent:
    def __init__(self, secret_path: str) -> None:
        self._secret_path = secret_path
        self._items: List[Dict[str, Any]] = []

    def enqueue(self, item: Dict[str, Any]) -> None:
        if "id" not in item:
            return
        self._items.append(item)

    def sync(self, node: str, provided_secret: str) -> int:
        if node != "replica":
            return 0

        expected_secret = load_secret(self._secret_path)

        synced = 0
        pending: List[Dict[str, Any]] = []

        for entry in self._items:
            if entry.get("secure") is True:
                if provided_secret == expected_secret:
                    synced += 1
                else:
                    pending.append(entry)
            else:
                synced += 1

        self._items = pending
        return synced