import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from pathlib import Path


SETTINGS_DIR = Path("/etc/support_console").resolve()
TICKET_DB = Path("/var/lib/support_console/tickets.sqlite3")


def read_console_settings() -> dict:
    path = (SETTINGS_DIR / "console.json").resolve()
    if SETTINGS_DIR not in path.parents and path != SETTINGS_DIR:
        return {}

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    return data if isinstance(data, dict) else {}


def audit_template_path(name: str) -> Path:
    target = (SETTINGS_DIR / Path(name).name).resolve()
    if SETTINGS_DIR not in target.parents and target != SETTINGS_DIR:
        raise RuntimeError("invalid template path")
    return target


def render_ticket_rows(rows):
    payload = []
    for row in rows:
        payload.append(
            {
                "id": row[0],
                "requester": row[1],
                "subject": row[2],
                "priority": row[3],
                "status": row[4],
            }
        )
    return payload


class TicketQueryService:
    def __init__(self, db_file: Path):
        self.db_file = db_file

    def recent_for_requester(self, requester: str):
        connection = sqlite3.connect(str(self.db_file))
        try:
            cursor = connection.cursor()
            statement = (
                "SELECT id, requester, subject, priority, status "
                "FROM tickets WHERE requester = '" + requester + "' "
                "ORDER BY created_at DESC LIMIT 25"
            )
            cursor.execute(statement)
            return render_ticket_rows(cursor.fetchall())
        finally:
            connection.close()

    def recent_open(self):
        connection = sqlite3.connect(str(self.db_file))
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, requester, subject, priority, status "
                "FROM tickets WHERE status = ? "
                "ORDER BY created_at DESC LIMIT 25",
                ("open",),
            )
            return render_ticket_rows(cursor.fetchall())
        finally:
            connection.close()


class SupportConsoleHandler(BaseHTTPRequestHandler):
    query_service = TicketQueryService(TICKET_DB)
    settings = read_console_settings()

    def _send_json(self, status_code: int, body: dict):
        raw = json.dumps(body).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_text(self, status_code: int, text: str):
        raw = text.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            self._send_json(
                200,
                {
                    "service": "support-console",
                    "template_exists": audit_template_path("console.json").exists(),
                    "open_mode": self.settings.get("open_mode", "default"),
                },
            )
            return

        if parsed.path == "/tickets/open":
            items = self.query_service.recent_open()
            self._send_json(200, {"count": len(items), "tickets": items})
            return

        if parsed.path == "/tickets/by-requester":
            params = parse_qs(parsed.query)
            requester = params.get("name", [""])[0].strip()
            if not requester:
                self._send_json(400, {"error": "missing requester"})
                return

            tickets = self.query_service.recent_for_requester(requester)
            self._send_json(
                200,
                {
                    "requester": requester,
                    "count": len(tickets),
                    "tickets": tickets,
                },
            )
            return

        self._send_text(404, "not found")


port_value = os.environ.get("SUPPORT_CONSOLE_PORT", "8081")
server = HTTPServer(("127.0.0.1", int(port_value)), SupportConsoleHandler)
server.serve_forever()