import os
import json
import hmac
import shutil
import sqlite3
import hashlib
import tempfile
import subprocess
from pathlib import Path
from zipfile import ZipFile
from collections import namedtuple
from typing import Dict, Any, Iterable, List


CollectedEvidence = namedtuple("CollectedEvidence", ["incident_id", "title", "attachment_name", "staged_file", "preview"])


def incident_package_api(state_root: Path):
    database_file = (state_root / "state" / "incident.sqlite3").resolve()
    template_root = (state_root / "templates").resolve()
    attachment_root = (state_root / "attachments").resolve()
    package_root = (state_root / "packages").resolve()
    work_root = (state_root / "work").resolve()

    def ensure_layout() -> None:
        template_root.mkdir(parents=True, exist_ok=True)
        attachment_root.mkdir(parents=True, exist_ok=True)
        package_root.mkdir(parents=True, exist_ok=True)
        work_root.mkdir(parents=True, exist_ok=True)
        database_file.parent.mkdir(parents=True, exist_ok=True)

    def parse_request(text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return {}

        return payload if isinstance(payload, dict) else {}

    def clamp_limit(value: object) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError):
            return 25

        if number < 1:
            return 1
        if number > 200:
            return 200
        return number

    def open_db() -> sqlite3.Connection:
        return sqlite3.connect(str(database_file))

    def load_template(name: str) -> str:
        template_file = (template_root / Path(name).name).resolve()
        if not template_file.exists():
            return ""

        try:
            with open(template_file, "r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError:
            return ""

        return content

    def find_incidents(connection: sqlite3.Connection, reporter: str, status: str, limit: int) -> List[Dict[str, Any]]:
        cursor = connection.cursor()

        statement = (
            "SELECT id, reporter, title, status, attachment_name "
            "FROM incidents "
            "WHERE reporter = '" + reporter + "' "
            "AND status = '" + status + "' "
            "ORDER BY created_at DESC "
            f"LIMIT {limit}"
        )

        cursor.execute(statement)
        rows = cursor.fetchall()

        incidents: List[Dict[str, Any]] = []
        for row in rows:
            incidents.append(
                {
                    "incident_id": row[0],
                    "reporter": row[1],
                    "title": row[2],
                    "status": row[3],
                    "attachment_name": row[4],
                }
            )

        return incidents

    def stage_attachment(workspace: Path, attachment_name: str) -> Path:
        source = (attachment_root / attachment_name).resolve()
        destination = (workspace / Path(attachment_name).name).resolve()

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    def preview_attachment(program: str, target: Path) -> Dict[str, Any]:
        command = f"{program} {target}"
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

        return {
            "exit_code": completed.returncode,
            "stdout_size": len(completed.stdout),
            "stderr_size": len(completed.stderr),
        }

    def allocate_workspace(batch_name: str) -> Path:
        prefix = f"{Path(batch_name).name}_"
        workspace = Path(tempfile.mkdtemp(prefix=prefix, dir=str(work_root))).resolve()
        if work_root not in workspace.parents and workspace != work_root:
            raise RuntimeError("invalid workspace")
        return workspace

    def assemble_rows(
        incidents: Iterable[Dict[str, Any]],
        workspace: Path,
        preview_program: str,
        template_text: str,
        operator: str,
    ) -> List[CollectedEvidence]:
        collected: List[CollectedEvidence] = []

        for incident in incidents:
            staged_file = stage_attachment(workspace, str(incident["attachment_name"]))
            preview = preview_attachment(preview_program, staged_file)

            title = str(incident["title"])
            note = template_text.replace("{{title}}", title).replace("{{operator}}", operator)

            collected.append(
                CollectedEvidence(
                    incident_id=int(incident["incident_id"]),
                    title=note,
                    attachment_name=Path(str(incident["attachment_name"])).name,
                    staged_file=staged_file,
                    preview=preview,
                )
            )

        return collected

    def manifest_document(batch_name: str, reporter: str, status: str, rows: Iterable[CollectedEvidence]) -> Dict[str, Any]:
        items: List[Dict[str, Any]] = []

        for row in rows:
            items.append(
                {
                    "incident_id": row.incident_id,
                    "title": row.title,
                    "attachment": row.attachment_name,
                    "preview": row.preview,
                }
            )

        secret = b"incident-package-signing-key"
        body = {
            "batch_name": batch_name,
            "reporter": reporter,
            "status": status,
            "item_count": len(items),
            "items": items,
        }
        raw = json.dumps(body, separators=(",", ":")).encode("utf-8")
        signature = hmac.new(secret, raw, hashlib.sha256).hexdigest()

        body["signature"] = signature
        return body

    def write_manifest(workspace: Path, document: Dict[str, Any]) -> Path:
        manifest_path = (workspace / "manifest.json").resolve()
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
        return manifest_path

    def package_output_path(file_name: str) -> Path:
        target = (package_root / Path(file_name).name).resolve()
        if package_root not in target.parents and target != package_root:
            raise RuntimeError("invalid package path")
        return target

    def write_archive(output_name: str, workspace: Path) -> Path:
        archive_path = package_output_path(output_name)

        with ZipFile(archive_path, "w") as archive:
            for entry in sorted(workspace.iterdir()):
                if entry.is_file():
                    archive.write(entry, arcname=entry.name)

        return archive_path

    def record_dispatch(connection: sqlite3.Connection, reporter: str, package_file: Path, item_count: int) -> None:
        connection.execute(
            "INSERT INTO incident_package_log(reporter, package_file, item_count) VALUES (?, ?, ?)",
            (reporter, str(package_file), item_count),
        )
        connection.commit()

    def handle(request_text: str) -> Dict[str, Any]:
        ensure_layout()

        request = parse_request(request_text)
        if not request:
            return {"error": "invalid request"}

        reporter = str(request.get("reporter", "")).strip()
        status = str(request.get("status", "open")).strip() or "open"
        batch_name = str(request.get("batch_name", "incident_batch")).strip() or "incident_batch"
        output_name = str(request.get("output_name", "incident_bundle.zip")).strip() or "incident_bundle.zip"
        template_name = str(request.get("template_name", "incident_note.txt")).strip() or "incident_note.txt"
        preview_program = str(request.get("preview_program", "file")).strip() or "file"
        operator = str(request.get("operator", "")).strip()
        limit = clamp_limit(request.get("limit"))

        if not reporter:
            return {"error": "missing reporter"}
        if not operator:
            return {"error": "missing operator"}

        workspace = allocate_workspace(batch_name)
        template_text = load_template(template_name)

        try:
            with open_db() as connection:
                incidents = find_incidents(connection, reporter, status, limit)
                if not incidents:
                    return {
                        "reporter": reporter,
                        "status": status,
                        "count": 0,
                        "package": None,
                    }

                rows = assemble_rows(incidents, workspace, preview_program, template_text, operator)
                document = manifest_document(batch_name, reporter, status, rows)
                write_manifest(workspace, document)

                package_file = write_archive(output_name, workspace)
                record_dispatch(connection, reporter, package_file, len(rows))

            return {
                "reporter": reporter,
                "status": status,
                "count": len(rows),
                "package": str(package_file),
            }
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

    return handle


handle_incident_package = incident_package_api(Path("/srv/incident_package"))