import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class ReviewWindow:
    def __init__(self, start: str, end: str):
        self.start = start.strip()
        self.end = end.strip()

    def as_sql_clause(self) -> str:
        parts: List[str] = []
        if self.start:
            parts.append(f"created_at >= '{self.start}'")
        if self.end:
            parts.append(f"created_at <= '{self.end}'")
        return " AND ".join(parts)


class NoteStore:
    def __init__(self, db_file: Path):
        self.db_file = db_file

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def load_recent_notes(self, author: str, window: ReviewWindow, limit: int) -> List[Tuple[int, str, str, str]]:
        connection = self._connect()
        try:
            cursor = connection.cursor()

            clauses = [f"author = '{author}'"]
            date_clause = window.as_sql_clause()
            if date_clause:
                clauses.append(date_clause)

            statement = (
                "SELECT id, author, title, body "
                "FROM review_notes "
                "WHERE " + " AND ".join(clauses) + " "
                "ORDER BY created_at DESC "
                f"LIMIT {limit}"
            )

            cursor.execute(statement)
            return cursor.fetchall()
        finally:
            connection.close()

    def load_ticket_status(self, ticket_id: int) -> Optional[str]:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT status FROM ticket_index WHERE id = ?",
                (ticket_id,),
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            connection.close()


class ExportLayout:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.reports = (self.root / "reports").resolve()
        self.templates = (self.root / "templates").resolve()

    def prepare(self) -> None:
        self.reports.mkdir(parents=True, exist_ok=True)
        self.templates.mkdir(parents=True, exist_ok=True)

    def template_path(self, name: str) -> Path:
        candidate = (self.templates / Path(name).name).resolve()
        if self.templates not in candidate.parents and candidate != self.templates:
            raise RuntimeError("invalid template path")
        return candidate

    def report_path(self, relative_name: str) -> Path:
        return (self.reports / relative_name).resolve()


class NoteExporter:
    def __init__(self, layout: ExportLayout):
        self.layout = layout

    def format_record(self, row: Tuple[int, str, str, str], ticket_status: Optional[str]) -> Dict[str, object]:
        return {
            "id": row[0],
            "author": row[1],
            "title": row[2],
            "body": row[3],
            "ticket_status": ticket_status or "unknown",
        }

    def build_payload(
        self,
        rows: List[Tuple[int, str, str, str]],
        status_lookup,
    ) -> Dict[str, object]:
        items: List[Dict[str, object]] = []
        for row in rows:
            items.append(self.format_record(row, status_lookup(row[0])))

        return {
            "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "count": len(items),
            "items": items,
        }

    def write_payload(self, target_name: str, payload: Dict[str, object]) -> Path:
        destination = self.layout.report_path(target_name)
        with open(destination, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        return destination


def parse_request(blob: str) -> Dict[str, object]:
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def clamp_limit(value: object) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 25

    if number < 1:
        return 1
    if number > 100:
        return 100
    return number


def render_console_message(author: str, file_path: Path, count: int) -> str:
    return json.dumps(
        {
            "author": author,
            "file": str(file_path),
            "count": count,
        },
        indent=2,
    )


workspace = Path("/srv/review_console")
layout = ExportLayout(workspace)
layout.prepare()

request_data = parse_request(os.environ.get("NOTE_EXPORT_REQUEST", "{}"))
database_path = Path("/srv/review_console/data/reviews.sqlite3")
store = NoteStore(database_path)

author_name = str(request_data.get("author", "")).strip()
start_date = str(request_data.get("start", "")).strip()
end_date = str(request_data.get("end", "")).strip()
export_name = str(request_data.get("export_name", "recent_notes.json")).strip()

if not author_name:
    print(json.dumps({"error": "missing author"}, indent=2))
else:
    review_window = ReviewWindow(start_date, end_date)
    rows = store.load_recent_notes(author_name, review_window, clamp_limit(request_data.get("limit")))
    payload = NoteExporter(layout).build_payload(rows, store.load_ticket_status)
    file_path = NoteExporter(layout).write_payload(export_name, payload)
    print(render_console_message(author_name, file_path, payload["count"]))