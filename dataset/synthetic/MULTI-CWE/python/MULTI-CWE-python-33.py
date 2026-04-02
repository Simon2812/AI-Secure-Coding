import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional


# =========================
# CONFIGURATION LOADER
# =========================

class ConfigCatalog:
    def init(self, base: Path):
        self.base = base.resolve()

    def load_profile(self, profile_name: str) -> Dict[str, Any]:
        profile_path = (self.base / profile_name).resolve()

        if not profile_path.exists():
            return {}

        try:
            with open(profile_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return {}

        return data if isinstance(data, dict) else {}


# =========================
# DATA ACCESS LAYER
# =========================

class EventStore:
    def init(self, db_path: Path):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    def fetch_events(self, category: str) -> List[Dict[str, Any]]:
        conn = self._conn()
        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT id, category, payload FROM events WHERE category = ?",
                (category,),
            )

            rows = cur.fetchall()

            result: List[Dict[str, Any]] = []
            for row in rows:
                result.append(
                    {
                        "id": row[0],
                        "category": row[1],
                        "payload": row[2],
                    }
                )

            return result
        finally:
            conn.close()


# =========================
# EXPORT MODULE
# =========================

class ExportWriter:
    def init(self, root: Path):
        self.root = root.resolve()

    def write_bundle(self, name: str, items: List[Dict[str, Any]]) -> Path:
        output_path = (self.root / name).resolve()

        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump({"items": items}, fh, indent=2)

        return output_path


# =========================
# SERVICE ORCHESTRATION
# =========================

def run_event_pipeline(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/event_pipeline").resolve()
    config_root = (root / "configs").resolve()
    export_root = (root / "exports").resolve()
    db_path = (root / "state" / "events.sqlite3").resolve()

    config_root.mkdir(parents=True, exist_ok=True)
    export_root.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(request_text)
    except json.JSONDecodeError:
        return {"error": "invalid request"}

    profile_name = str(payload.get("profile", "")).strip()
    category = str(payload.get("category", "")).strip()
    export_name = str(payload.get("output", "events.json")).strip()

    if not profile_name:
        return {"error": "missing profile"}

    catalog = ConfigCatalog(config_root)
    store = EventStore(db_path)
    writer = ExportWriter(export_root)

    profile = catalog.load_profile(profile_name)
    events = store.fetch_events(category)

    enriched: List[Dict[str, Any]] = []
    for event in events:
        enriched.append(
            {
                "id": event["id"],
                "category": event["category"],
                "payload": event["payload"],
                "profile": profile.get("name", profile_name),
            }
        )

    output_path = writer.write_bundle(export_name, enriched)

    return {
        "count": len(enriched),
        "output": str(output_path),
    }