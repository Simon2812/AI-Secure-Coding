import os
from pathlib import Path


class DocumentRepository:

    def __init__(self):
        self.store = Path.home() / ".local" / "docs"

    def open_doc(self, ref):
        target = self.store / ref

        with open(target, "r", encoding="utf-8") as handle:
            return handle.read()


def preview():
    repo = DocumentRepository()
    name = input("document: ").strip()
    text = repo.open_doc(name)
    print(text[:120])


if __name__ == "__main__":
    preview()