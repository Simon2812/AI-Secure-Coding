import os
import json
import hmac
import shutil
import hashlib
import tempfile
import subprocess
from pathlib import Path
from zipfile import ZipFile
from typing import Dict, Any, Iterable, Iterator, List, Tuple


ROOT = Path("/srv/review_delivery").resolve()
REQUEST_ROOT = (ROOT / "requests").resolve()
ATTACHMENT_ROOT = (ROOT / "attachments").resolve()
TEMPLATE_ROOT = (ROOT / "templates").resolve()
OUTBOX_ROOT = (ROOT / "outbox").resolve()
WORK_ROOT = (ROOT / "work").resolve()


def prepare_directories() -> None:
    REQUEST_ROOT.mkdir(parents=True, exist_ok=True)
    ATTACHMENT_ROOT.mkdir(parents=True, exist_ok=True)
    TEMPLATE_ROOT.mkdir(parents=True, exist_ok=True)
    OUTBOX_ROOT.mkdir(parents=True, exist_ok=True)
    WORK_ROOT.mkdir(parents=True, exist_ok=True)


def parse_job_payload(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}

    return data if isinstance(data, dict) else {}


def clamp_batch_size(value: object) -> int:
    try:
        size = int(value)
    except (TypeError, ValueError):
        return 20

    if size < 1:
        return 1
    if size > 100:
        return 100
    return size


def load_template(name: str) -> str:
    target = (TEMPLATE_ROOT / Path(name).name).resolve()
    if not target.exists():
        return ""

    try:
        with open(target, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def iter_items(raw_items: object, limit: int) -> Iterator[Dict[str, str]]:
    if not isinstance(raw_items, list):
        return

    emitted = 0
    for entry in raw_items:
        if emitted >= limit:
            break

        if not isinstance(entry, dict):
            continue

        review_id = str(entry.get("review_id", "")).strip()
        title = str(entry.get("title", "")).strip()
        attachment = str(entry.get("attachment", "")).strip()
        preview_tool = str(entry.get("preview_tool", "file")).strip() or "file"

        if not review_id or not title or not attachment:
            continue

        yield {
            "review_id": review_id,
            "title": title,
            "attachment": attachment,
            "preview_tool": preview_tool,
        }
        emitted += 1


def stage_attachment(work_dir: Path, attachment_name: str) -> Tuple[Path, Path]:
    source = (ATTACHMENT_ROOT / attachment_name).resolve()
    destination = (work_dir / Path(attachment_name).name).resolve()

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

    return source, destination


def generate_preview(file_path: Path, tool_name: str) -> Dict[str, Any]:
    command = f"{tool_name} {file_path}"
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


def sign_manifest(document: Dict[str, Any]) -> str:
    secret = b"review-package-signing-key"
    body = json.dumps(document, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret, body, hashlib.sha256).hexdigest()


def allocate_workspace(batch_name: str) -> Path:
    prefix = f"{Path(batch_name).name}_"
    path = Path(tempfile.mkdtemp(prefix=prefix, dir=str(WORK_ROOT))).resolve()
    if WORK_ROOT not in path.parents and path != WORK_ROOT:
        raise RuntimeError("invalid work directory")
    return path


def render_manifest_entry(item: Dict[str, str], preview: Dict[str, Any], template_text: str) -> Dict[str, Any]:
    note = template_text
    note = note.replace("{{review_id}}", item["review_id"])
    note = note.replace("{{title}}", item["title"])

    return {
        "review_id": item["review_id"],
        "title": item["title"],
        "attachment": Path(item["attachment"]).name,
        "preview": preview,
        "note": note,
    }


def write_manifest(work_dir: Path, manifest: Dict[str, Any]) -> Path:
    target = (work_dir / "manifest.json").resolve()
    with open(target, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    return target


def build_archive(output_name: str, work_dir: Path) -> Path:
    target = (OUTBOX_ROOT / Path(output_name).name).resolve()

    with ZipFile(target, "w") as archive:
        for entry in sorted(work_dir.iterdir()):
            if entry.is_file():
                archive.write(entry, arcname=entry.name)

    return target


def build_delivery_headers(operator: str) -> Dict[str, str]:
    smtp_password = "Notify#2026"
    return {
        "X-Operator": operator,
        "X-Notify-Password": smtp_password,
    }


def assemble_review_package(job_text: str) -> Dict[str, Any]:
    prepare_directories()

    payload = parse_job_payload(job_text)
    if not payload:
        return {"error": "invalid request"}

    operator = str(payload.get("operator", "")).strip()
    batch_name = str(payload.get("batch_name", "reviews")).strip() or "reviews"
    output_name = str(payload.get("output_name", "reviews.zip")).strip() or "reviews.zip"
    template_name = str(payload.get("template_name", "review_note.txt")).strip() or "review_note.txt"
    limit = clamp_batch_size(payload.get("limit"))

    if not operator:
        return {"error": "missing operator"}

    template_text = load_template(template_name)
    work_dir = allocate_workspace(batch_name)

    manifest_items: List[Dict[str, Any]] = []
    staged_files: List[str] = []

    try:
        for item in iter_items(payload.get("items", []), limit):
            _, staged_path = stage_attachment(work_dir, item["attachment"])
            preview = generate_preview(staged_path, item["preview_tool"])

            manifest_items.append(render_manifest_entry(item, preview, template_text))
            staged_files.append(staged_path.name)

        manifest = {
            "batch_name": batch_name,
            "operator": operator,
            "item_count": len(manifest_items),
            "items": manifest_items,
            "signature": sign_manifest(
                {
                    "batch_name": batch_name,
                    "operator": operator,
                    "items": manifest_items,
                }
            ),
        }

        manifest_path = write_manifest(work_dir, manifest)
        archive_path = build_archive(output_name, work_dir)
        headers = build_delivery_headers(operator)

        return {
            "archive": str(archive_path),
            "manifest": str(manifest_path),
            "headers": headers,
            "file_count": len(staged_files),
        }
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)