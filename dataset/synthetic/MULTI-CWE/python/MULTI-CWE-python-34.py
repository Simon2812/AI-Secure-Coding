import os
import json
import shutil
import sqlite3
import tarfile
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, Iterable, List, Tuple


# =========================
# DATA ACCESS (separate, safe)
# =========================

class ReviewIndex:
    def init(self, db_file: Path):
        self.db_file = db_file

    def _connect(self):
        return sqlite3.connect(str(self.db_file))

    def reviewer_summary(self) -> List[Tuple[str, int]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT reviewer, COUNT(*) FROM review_queue GROUP BY reviewer"
            )
            return [(r[0], r[1]) for r in cur.fetchall()]
        finally:
            conn.close()


# =========================
# ARTIFACT HANDLING
# =========================

class ArtifactShelf:
    def init(self, root: Path):
        self.root = root.resolve()

    def resolve(self, name: str) -> Path:
        return (self.root / Path(name).name).resolve()


def copy_artifact(src: Path, workspace: Path) -> Path:
    dst = (workspace / src.name).resolve()
    shutil.copy2(src, dst)
    return dst


# =========================
# VULNERABLE EXECUTION FLOW
# =========================

class PackagingStage:
    def init(self, workspace: Path):
        self.workspace = workspace

    # ---- VULN PART 1 (command construction)
    def build_command(self, tool_name: str, target: Path) -> str:
        return f"{tool_name} {target}"

    # ---- VULN PART 2 (execution)
    def execute(self, command: str) -> Dict[str, Any]:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=str(self.workspace),
            capture_output=True,
            text=True,
        )
        return {
            "exit_code": proc.returncode,
            "stderr_size": len(proc.stderr),
        }


# =========================
# MANIFEST
# =========================

def write_manifest(path: Path, items: Iterable[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"items": list(items)}, fh, indent=2)


# =========================
# ENTRY POINT
# =========================

def assemble_release(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/release_builder").resolve()
    artifact_root = (root / "artifacts").resolve()
    workspace_root = (root / "workspace").resolve()
    db_file = (root / "state" / "release.sqlite3").resolve()

    artifact_root.mkdir(parents=True, exist_ok=True)
    workspace_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(request_text)
    except json.JSONDecodeError:
        return {"error": "invalid"}

    entries = payload.get("entries", [])
    tool = str(payload.get("tool", "file")).strip()

    if not isinstance(entries, list) or not entries:
        return {"error": "no entries"}

    workspace = Path(tempfile.mkdtemp(dir=str(workspace_root))).resolve()

    shelf = ArtifactShelf(artifact_root)
    stage = PackagingStage(workspace)
    index = ReviewIndex(db_file)

    results: List[Dict[str, Any]] = []

    try:
        for entry in entries:
            if not isinstance(entry, dict):
                continue

            name = str(entry.get("artifact", "")).strip()
            if not name:
                continue

            src = shelf.resolve(name)
            staged = copy_artifact(src, workspace)

            # ---- VULN CHAIN ----
            cmd = stage.build_command(tool, staged)
            execution = stage.execute(cmd)

            results.append(
                {
                    "artifact": staged.name,
                    "execution": execution,
                }
            )

        manifest_path = (workspace / "manifest.json").resolve()
        write_manifest(manifest_path, results)

        reviewers = index.reviewer_summary()
        return {
            "items": len(results),
            "manifest": str(manifest_path),
            "reviewers": reviewers,
        }

    finally:
        shutil.rmtree(workspace, ignore_errors=True)