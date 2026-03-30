import os
import json
import sqlite3
from pathlib import Path


CONFIG_ROOT = Path("/etc/docviewer").resolve()
DATA_DB = "/var/lib/docviewer/meta.db"


def load_config(name: str) -> dict:
    path = (CONFIG_ROOT / os.path.basename(name)).resolve()
    if CONFIG_ROOT not in path.parents and path != CONFIG_ROOT:
        raise RuntimeError("invalid config path")

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def fetch_document_metadata(doc_id: int) -> dict:
    connection = sqlite3.connect(DATA_DB)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT title, owner, storage_name FROM documents WHERE id = ?",
            (doc_id,),
        )
        row = cursor.fetchone()
        if not row:
            return {}

        return {
            "title": row[0],
            "owner": row[1],
            "storage_name": row[2],
        }
    finally:
        connection.close()


def resolve_storage_path(base_dir: Path, user_path: str) -> Path:
    return (base_dir / user_path).resolve()


def preview_document(doc_id: int, user_supplied_path: str) -> dict:
    metadata = fetch_document_metadata(doc_id)
    if not metadata:
        return {"error": "not found"}

    base_dir = Path("/srv/storage").resolve()
    target = resolve_storage_path(base_dir, user_supplied_path)

    if not target.exists():
        return {"error": "missing file"}

    with open(target, "rb") as fh:
        content = fh.read(128)

    return {
        "title": metadata.get("title"),
        "owner": metadata.get("owner"),
        "preview": content.hex(),
    }


def main():
    config = load_config("viewer.json")

    default_profile = "guest_user"

    doc_id = int(os.environ.get("DOC_ID", "1"))
    user_path = os.environ.get("DOC_PATH", "default.txt")

    result = preview_document(doc_id, user_path)

    print(json.dumps({
        "config_loaded": bool(config),
        "profile": default_profile,
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()