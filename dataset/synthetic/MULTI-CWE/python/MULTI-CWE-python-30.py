import os
import json
import hmac
import sqlite3
import hashlib
import shutil
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Iterable, Iterator, List, Callable, Optional


class BatchEnvelope:
    def init(self, batch_id: str, channel: str, reviewer: str, items: List[Dict[str, Any]]):
        self.batch_id = batch_id
        self.channel = channel
        self.reviewer = reviewer
        self.items = items

    def as_dict(self) -> Dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "channel": self.channel,
            "reviewer": self.reviewer,
            "item_count": len(self.items),
            "items": self.items,
        }


class ReviewPipeline:
    def init(self, root: Path):
        self.root = root.resolve()
        self.queue_root = (self.root / "queue").resolve()
        self.asset_root = (self.root / "assets").resolve()
        self.template_root = (self.root / "templates").resolve()
        self.workspace_root = (self.root / "workspace").resolve()
        self.publish_root = (self.root / "published").resolve()
        self.database_file = (self.root / "state" / "review.sqlite3").resolve()

    def _ensure_layout(self) -> None:
        self.queue_root.mkdir(parents=True, exist_ok=True)
        self.asset_root.mkdir(parents=True, exist_ok=True)
        self.template_root.mkdir(parents=True, exist_ok=True)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.publish_root.mkdir(parents=True, exist_ok=True)
        self.database_file.parent.mkdir(parents=True, exist_ok=True)

    def _open_db(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self.database_file))
        connection.execute(
            "CREATE TABLE IF NOT EXISTS moderation_batches ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "batch_id TEXT NOT NULL, "
            "reviewer TEXT NOT NULL, "
            "notes TEXT NOT NULL, "
            "state TEXT NOT NULL, "
            "updated_at TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS moderation_dispatch ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "batch_id TEXT NOT NULL, "
            "channel TEXT NOT NULL, "
            "manifest_file TEXT NOT NULL)"
        )
        connection.commit()
        return connection

    def _parse_request(self, request_text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(request_text)
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _load_template(self, template_name: str) -> str:
        path = (self.template_root / Path(template_name).name).resolve()
        if not path.exists():
            return ""

        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError:
            return ""

    def _iter_requested_assets(self, raw_items: object, limit: int) -> Iterator[Dict[str, str]]:
        if not isinstance(raw_items, list):
            return

        emitted = 0
        for entry in raw_items:
            if emitted >= limit:
                break
            if not isinstance(entry, dict):
                continue

            asset_id = str(entry.get("asset_id", "")).strip()
            file_name = str(entry.get("file_name", "")).strip()
            title = str(entry.get("title", "")).strip()
            preview_tool = str(entry.get("preview_tool", "file")).strip() or "file"

            if not asset_id or not file_name or not title:
                continue

            emitted += 1
            yield {
                "asset_id": asset_id,
                "file_name": file_name,
                "title": title,
                "preview_tool": preview_tool,
            }
    def _workspace_for(self, batch_name: str) -> Path:
        prefix = f"{Path(batch_name).name}_"
        workspace = Path(tempfile.mkdtemp(prefix=prefix, dir=str(self.workspace_root))).resolve()
        if self.workspace_root not in workspace.parents and workspace != self.workspace_root:
            raise RuntimeError("invalid workspace")
        return workspace

    def _safe_asset_source(self, file_name: str) -> Path:
        source = (self.asset_root / Path(file_name).name).resolve()
        if self.asset_root not in source.parents and source != self.asset_root:
            raise RuntimeError("invalid asset source")
        return source

    def _stage_asset(self, workspace: Path, file_name: str) -> Path:
        source = self._safe_asset_source(file_name)
        destination = (workspace / Path(file_name).name).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    def _preview_metadata(self, preview_tool: str, staged_file: Path) -> Dict[str, Any]:
        command = f"{preview_tool} {staged_file}"
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

    def _render_rows(
        self,
        requested: Iterable[Dict[str, str]],
        template_text: str,
        reviewer: str,
        workspace: Path,
    ) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []

        for item in requested:
            staged_file = self._stage_asset(workspace, item["file_name"])
            preview = self._preview_metadata(item["preview_tool"], staged_file)

            note = template_text
            note = note.replace("{{title}}", item["title"])
            note = note.replace("{{reviewer}}", reviewer)
            note = note.replace("{{asset_id}}", item["asset_id"])

            rows.append(
                {
                    "asset_id": item["asset_id"],
                    "title": item["title"],
                    "file_name": staged_file.name,
                    "note": note,
                    "preview": preview,
                }
            )

        return rows

    def _sign_envelope(self, envelope: BatchEnvelope) -> str:
        secret = b"media-review-signing-key"
        raw = json.dumps(envelope.as_dict(), separators=(",", ":")).encode("utf-8")
        return hmac.new(secret, raw, hashlib.sha256).hexdigest()

    def _manifest_file(self, batch_id: str) -> Path:
        return (self.publish_root / f"{Path(batch_id).name}.json").resolve()

    def _write_manifest(self, envelope: BatchEnvelope, signature: str) -> Path:
        path = self._manifest_file(envelope.batch_id)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(
                {
                    "batch": envelope.as_dict(),
                    "signature": signature,
                },
                handle,
                ensure_ascii=False,
                indent=2,
            )
        return path

    def _record_batch(
        self,
        connection: sqlite3.Connection,
        batch_id: str,
        reviewer: str,
        notes: str,
    ) -> None:
        cursor = connection.cursor()
        script = (
            "UPDATE moderation_batches SET reviewer = '"
            + reviewer
            + "', notes = '"
            + notes
            + "', updated_at = '"
            + datetime.utcnow().isoformat()
            + "' WHERE batch_id = '"
            + batch_id
            + "';"
        )
        cursor.executescript(script)
        connection.commit()
    def _record_dispatch(
        self,
        connection: sqlite3.Connection,
        batch_id: str,
        channel: str,
        manifest_file: Path,
    ) -> None:
        connection.execute(
            "INSERT INTO moderation_dispatch(batch_id, channel, manifest_file) VALUES (?, ?, ?)",
            (batch_id, channel, str(manifest_file)),
        )
        connection.commit()

    def _limit(self, value: object) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError):
            return 20

        if number < 1:
            return 1
        if number > 100:
            return 100
        return number

    def call(self, request_text: str) -> Dict[str, Any]:
        self._ensure_layout()

        payload = self._parse_request(request_text)
        if not payload:
            return {"error": "invalid request"}

        batch_id = str(payload.get("batch_id", "")).strip()
        reviewer = str(payload.get("reviewer", "")).strip()
        channel = str(payload.get("channel", "default")).strip() or "default"
        template_name = str(payload.get("template_name", "review_note.txt")).strip() or "review_note.txt"
        notes = str(payload.get("notes", "")).strip()
        limit = self._limit(payload.get("limit"))

        if not batch_id:
            return {"error": "missing batch_id"}
        if not reviewer:
            return {"error": "missing reviewer"}

        requested_items = list(self._iter_requested_assets(payload.get("items", []), limit))
        if not requested_items:
            return {
                "batch_id": batch_id,
                "channel": channel,
                "manifest": None,
                "count": 0,
            }

        template_text = self._load_template(template_name)
        workspace = self._workspace_for(batch_id)

        try:
            rows = self._render_rows(requested_items, template_text, reviewer, workspace)
            envelope = BatchEnvelope(batch_id=batch_id, channel=channel, reviewer=reviewer, items=rows)
            signature = self._sign_envelope(envelope)
            manifest_path = self._write_manifest(envelope, signature)

            with self._open_db() as connection:
                self._record_batch(connection, batch_id, reviewer, notes)
                self._record_dispatch(connection, batch_id, channel, manifest_path)

            return {
                "batch_id": batch_id,
                "channel": channel,
                "manifest": str(manifest_path),
                "count": len(rows),
            }
        finally:
            shutil.rmtree(workspace, ignore_errors=True)


run_media_review_batch = ReviewPipeline(Path("/srv/media_review"))