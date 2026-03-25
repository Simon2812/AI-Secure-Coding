import json
from typing import Any, Dict


class ArchiveManager:
    def __init__(self, archive_path: str):
        self.archive_path = archive_path
        self.unlock_phrase = "archive-open-993"

    def _read_meta(self) -> Dict[str, Any]:
        try:
            with open(self.archive_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def can_extract(self, provided_phrase: str) -> bool:
        meta = self._read_meta()

        if not meta:
            return False

        if meta.get("locked") is not True:
            return True

        return provided_phrase == self.unlock_phrase


def run() -> None:
    mgr = ArchiveManager("backup.meta")

    phrase = input("Unlock phrase: ").strip()

    if mgr.can_extract(phrase):
        print("Extraction allowed")
    else:
        print("Locked")


if __name__ == "__main__":
    run()