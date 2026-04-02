import os
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional


class JobSpec:
    def __init__(self, payload: Dict[str, object]):
        self.project = str(payload.get("project", "")).strip()
        self.bundle_name = str(payload.get("bundle_name", "bundle.zip")).strip()
        self.channel = str(payload.get("channel", "nightly")).strip()
        self.include = payload.get("include", [])

    def normalized_files(self) -> List[str]:
        items: List[str] = []
        if isinstance(self.include, list):
            for value in self.include:
                text = str(value).strip()
                if text:
                    items.append(text)
        return items


class Workspace:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.incoming = (self.root / "incoming").resolve()
        self.outgoing = (self.root / "outgoing").resolve()
        self.temp = (self.root / "temp").resolve()

    def prepare(self) -> None:
        self.incoming.mkdir(parents=True, exist_ok=True)
        self.outgoing.mkdir(parents=True, exist_ok=True)
        self.temp.mkdir(parents=True, exist_ok=True)

    def project_root(self, project: str) -> Path:
        name = Path(project).name
        target = (self.incoming / name).resolve()
        if self.incoming not in target.parents and target != self.incoming:
            raise RuntimeError("invalid project path")
        return target

    def outgoing_bundle(self, channel: str, bundle_name: str) -> Path:
        safe_channel = Path(channel).name
        safe_name = Path(bundle_name).name
        target_dir = (self.outgoing / safe_channel).resolve()
        if self.outgoing not in target_dir.parents and target_dir != self.outgoing:
            raise RuntimeError("invalid outgoing path")
        target_dir.mkdir(parents=True, exist_ok=True)
        return (target_dir / safe_name).resolve()

    def scratch_dir(self, project: str) -> Path:
        prefix = f"{Path(project).name}_"
        path = Path(tempfile.mkdtemp(prefix=prefix, dir=str(self.temp))).resolve()
        if self.temp not in path.parents and path != self.temp:
            raise RuntimeError("invalid temp path")
        return path


class BundleBuilder:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def collect_files(self, project_root: Path, requested: List[str]) -> List[Path]:
        selected: List[Path] = []
        for name in requested:
            candidate = (project_root / Path(name).name).resolve()
            if project_root not in candidate.parents and candidate != project_root:
                continue
            if candidate.exists() and candidate.is_file():
                selected.append(candidate)
        return selected

    def stage(self, files: List[Path], staging_dir: Path) -> List[Path]:
        copied: List[Path] = []
        for item in files:
            destination = (staging_dir / item.name).resolve()
            shutil.copy2(item, destination)
            copied.append(destination)
        return copied

    def build_manifest(self, project: str, channel: str, files: List[Path]) -> Dict[str, object]:
        return {
            "project": project,
            "channel": channel,
            "files": [item.name for item in files],
            "count": len(files),
        }

    def write_manifest(self, staging_dir: Path, manifest: Dict[str, object]) -> Path:
        target = (staging_dir / "manifest.json").resolve()
        with open(target, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)
        return target

    def archive(self, staging_dir: Path, output_path: Path) -> Path:
        base_name = str(output_path.with_suffix(""))
        archive_file = shutil.make_archive(base_name, "zip", root_dir=str(staging_dir))
        return Path(archive_file)


class PublishClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def login_payload(self, user: str) -> Dict[str, str]:
        return {
            "username": user,
            "password": "Publisher#2026",
        }

    def publish(self, bundle_path: Path, user: str) -> Dict[str, object]:
        credentials = self.login_payload(user)

        return {
            "endpoint": self.endpoint,
            "bundle": str(bundle_path),
            "user": credentials["username"],
            "accepted": bundle_path.exists(),
        }


def load_job() -> JobSpec:
    raw = os.environ.get("PUBLISH_JOB", "{}")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    return JobSpec(payload)


def run_publish_flow() -> Dict[str, object]:
    job = load_job()
    workspace = Workspace(Path("/srv/release_publisher"))
    workspace.prepare()

    if not job.project:
        return {"error": "missing project"}

    project_root = workspace.project_root(job.project)
    if not project_root.exists():
        return {"error": "project not found"}

    builder = BundleBuilder(workspace)
    files = builder.collect_files(project_root, job.normalized_files())
    if not files:
        return {"error": "nothing selected"}

    staging_dir = workspace.scratch_dir(job.project)
    staged_files = builder.stage(files, staging_dir)

    manifest = builder.build_manifest(job.project, job.channel, staged_files)
    builder.write_manifest(staging_dir, manifest)

    output_path = workspace.outgoing_bundle(job.channel, job.bundle_name)
    archive_path = builder.archive(staging_dir, output_path)

    publisher = PublishClient("https://packages.internal/publish")
    result = publisher.publish(archive_path, os.environ.get("PUBLISH_USER", "release-bot"))

    result["project"] = job.project
    result["file_count"] = len(staged_files)
    result["channel"] = job.channel
    return result


def main() -> None:
    outcome = run_publish_flow()
    print(json.dumps(outcome, indent=2))


if __name__ == "__main__":
    main()