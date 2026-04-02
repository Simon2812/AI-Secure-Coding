import os
import json
import base64
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Iterable, Optional
from zipfile import ZipFile

from Crypto.Cipher import ARC4


@dataclass
class PackageRequest:
    tenant: str
    operator: str
    category: str
    export_name: str
    template_name: str
    archive_name: str
    max_items: int

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "PackageRequest":
        tenant = str(payload.get("tenant", "")).strip()
        operator = str(payload.get("operator", "")).strip()
        category = str(payload.get("category", "general")).strip() or "general"
        export_name = str(payload.get("export_name", "bundle.json")).strip() or "bundle.json"
        template_name = str(payload.get("template_name", "summary.txt")).strip() or "summary.txt"
        archive_name = str(payload.get("archive_name", "bundle.zip")).strip() or "bundle.zip"

        try:
            max_items = int(payload.get("max_items", 25))
        except (TypeError, ValueError):
            max_items = 25

        if max_items < 1:
            max_items = 1
        if max_items > 200:
            max_items = 200

        return cls(
            tenant=tenant,
            operator=operator,
            category=category,
            export_name=export_name,
            template_name=template_name,
            archive_name=archive_name,
            max_items=max_items,
        )


@dataclass
class ContentRow:
    item_id: int
    tenant: str
    title: str
    body: str
    local_name: str


ROOT = Path("/srv/content_packager").resolve()
DB_FILE = ROOT / "state" / "content.sqlite3"
EXPORT_ROOT = (ROOT / "exports").resolve()
TEMPLATE_ROOT = (ROOT / "templates").resolve()
ARCHIVE_ROOT = (ROOT / "archives").resolve()
ATTACHMENT_ROOT = (ROOT / "attachments").resolve()


def ensure_layout() -> None:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    TEMPLATE_ROOT.mkdir(parents=True, exist_ok=True)
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    ATTACHMENT_ROOT.mkdir(parents=True, exist_ok=True)
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def parse_payload(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}

    return data if isinstance(data, dict) else {}


def open_database() -> sqlite3.Connection:
    return sqlite3.connect(str(DB_FILE))


def fetch_content_rows(
    connection: sqlite3.Connection,
    tenant: str,
    category: str,
    limit: int,
) -> List[ContentRow]:
    cursor = connection.cursor()

    statement = (
        "SELECT id, tenant, title, body, local_name "
        "FROM content_items "
        "WHERE tenant = '" + tenant + "' "
        "AND category = '" + category + "' "
        "ORDER BY created_at DESC "
        f"LIMIT {limit}"
    )

    cursor.execute(statement)
    rows = cursor.fetchall()

    items: List[ContentRow] = []
    for row in rows:
        items.append(
            ContentRow(
                item_id=row[0],
                tenant=row[1],
                title=row[2],
                body=row[3],
                local_name=row[4],
            )
        )
    return items


def load_template_text(name: str) -> str:
    path = (TEMPLATE_ROOT / Path(name).name).resolve()
    if not path.exists():
        return ""

    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def render_summary(rows: Iterable[ContentRow], template_text: str, operator: str) -> List[Dict[str, Any]]:
    rendered: List[Dict[str, Any]] = []

    for row in rows:
        note = template_text
        note = note.replace("{{title}}", row.title)
        note = note.replace("{{tenant}}", row.tenant)
        note = note.replace("{{operator}}", operator)

        rendered.append(
            {
                "id": row.item_id,
                "title": row.title,
                "note": note,
                "attachment": row.local_name,
            }
        )

    return rendered


def attachment_path(local_name: str) -> Path:
    return (ATTACHMENT_ROOT / local_name).resolve()


def collect_existing_attachments(rows: Iterable[ContentRow]) -> List[Path]:
    found: List[Path] = []

    for row in rows:
        path = attachment_path(row.local_name)
        if path.exists() and path.is_file():
            found.append(path)

    return found


def encrypt_bundle(document: Dict[str, Any], secret: bytes) -> str:
    raw = json.dumps(document, separators=(",", ":")).encode("utf-8")
    cipher = ARC4.new(secret)
    encrypted = cipher.encrypt(raw)
    return base64.b64encode(encrypted).decode("utf-8")


def export_document_path(name: str) -> Path:
    return (EXPORT_ROOT / Path(name).name).resolve()


def archive_output_path(name: str) -> Path:
    return (ARCHIVE_ROOT / Path(name).name).resolve()


def write_export_file(path: Path, document: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(document, handle, ensure_ascii=False, indent=2)


def build_archive(archive_path: Path, export_path: Path, attachments: Iterable[Path]) -> None:
    with ZipFile(archive_path, "w") as archive:
        archive.write(export_path, arcname=export_path.name)

        for attachment in attachments:
            archive.write(attachment, arcname=attachment.name)


def update_dispatch_log(connection: sqlite3.Connection, tenant: str, export_path: Path, item_count: int) -> None:
    connection.execute(
        "INSERT INTO package_log(tenant, export_path, item_count) VALUES (?, ?, ?)",
        (tenant, str(export_path), item_count),
    )
    connection.commit()


def package_content(request_text: str) -> Dict[str, Any]:
    ensure_layout()

    request = PackageRequest.from_payload(parse_payload(request_text))
    if not request.tenant:
        return {"error": "missing tenant"}
    if not request.operator:
        return {"error": "missing operator"}

    template_text = load_template_text(request.template_name)

    secret = b"package-export-key"

    with open_database() as connection:
        rows = fetch_content_rows(connection, request.tenant, request.category, request.max_items)

        if not rows:
            return {
                "tenant": request.tenant,
                "category": request.category,
                "items": 0,
                "archive": None,
            }

        rendered = render_summary(rows, template_text, request.operator)
        attachments = collect_existing_attachments(rows)

        document = {
            "tenant": request.tenant,
            "category": request.category,
            "operator": request.operator,
            "count": len(rendered),
            "items": rendered,
            "payload": encrypt_bundle(
                {
                    "tenant": request.tenant,
                    "items": rendered,
                },
                secret,
            ),
        }

        export_path = export_document_path(request.export_name)
        write_export_file(export_path, document)

        archive_path = archive_output_path(request.archive_name)
        build_archive(archive_path, export_path, attachments)

        update_dispatch_log(connection, request.tenant, export_path, len(rendered))

    return {
        "tenant": request.tenant,
        "category": request.category,
        "items": len(rendered),
        "archive": str(archive_path),
        "export": str(export_path),
    }