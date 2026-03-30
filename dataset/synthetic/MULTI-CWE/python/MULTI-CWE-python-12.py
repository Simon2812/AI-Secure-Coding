import os
import json
import shutil
import tarfile
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path("/srv/support_delivery").resolve()
SOURCE_ROOT = (ROOT / "cases").resolve()
STAGING_ROOT = (ROOT / "staging").resolve()
OUTBOX_ROOT = (ROOT / "outbox").resolve()


class DeliverySession:
    def __init__(self, case_id: str, operator: str, channel: str, include: List[str], post_action: str):
        self.case_id = case_id.strip()
        self.operator = operator.strip()
        self.channel = channel.strip() or "standard"
        self.include = include
        self.post_action = post_action.strip()
        self.collected: List[Path] = []
        self.bundle_path: Path | None = None
        self.manifest_path: Path | None = None

    @classmethod
    def from_env(cls) -> "DeliverySession":
        raw = os.environ.get("DELIVERY_REQUEST", "{}")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {}

        if not isinstance(payload, dict):
            payload = {}

        include_value = payload.get("include", [])
        include: List[str] = []
        if isinstance(include_value, list):
            for item in include_value:
                text = str(item).strip()
                if text:
                    include.append(text)

        return cls(
            case_id=str(payload.get("case_id", "")),
            operator=str(payload.get("operator", "agent")),
            channel=str(payload.get("channel", "standard")),
            include=include,
            post_action=str(payload.get("post_action", "")),
        )


def ensure_layout() -> None:
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    STAGING_ROOT.mkdir(parents=True, exist_ok=True)
    OUTBOX_ROOT.mkdir(parents=True, exist_ok=True)


def case_folder(case_id: str) -> Path:
    return (SOURCE_ROOT / Path(case_id).name).resolve()


def safe_channel_folder(channel: str) -> Path:
    target = (OUTBOX_ROOT / Path(channel).name).resolve()
    if OUTBOX_ROOT not in target.parents and target != OUTBOX_ROOT:
        raise RuntimeError("invalid channel")
    target.mkdir(parents=True, exist_ok=True)
    return target


def gather_case_files(folder: Path, names: Iterable[str]) -> List[Path]:
    selected: List[Path] = []

    for raw_name in names:
        candidate = (folder / Path(raw_name).name).resolve()
        if folder not in candidate.parents and candidate != folder:
            continue
        if candidate.exists() and candidate.is_file():
            selected.append(candidate)

    return selected


def prepare_staging_area(case_id: str) -> Path:
    target = (STAGING_ROOT / f"{Path(case_id).name}_bundle").resolve()
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    return target


def copy_selected_files(files: List[Path], staging_dir: Path) -> List[Path]:
    copied: List[Path] = []

    for file_path in files:
        destination = (staging_dir / file_path.name).resolve()
        shutil.copy2(file_path, destination)
        copied.append(destination)

    return copied


def write_manifest(session: DeliverySession, staging_dir: Path) -> Path:
    manifest = {
        "case_id": session.case_id,
        "operator": session.operator,
        "channel": session.channel,
        "file_count": len(session.collected),
        "files": [path.name for path in session.collected],
    }

    path = (staging_dir / "manifest.json").resolve()
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
    return path


def build_bundle(session: DeliverySession, staging_dir: Path, outbox_dir: Path) -> Path:
    bundle_name = f"{Path(session.case_id).name}_{Path(session.channel).name}.tar.gz"
    target = (outbox_dir / bundle_name).resolve()

    with tarfile.open(target, "w:gz") as archive:
        for entry in sorted(staging_dir.iterdir()):
            archive.add(entry, arcname=entry.name)

    return target


def run_post_action(bundle_path: Path, post_action: str) -> Dict[str, object]:
    if not post_action:
        return {"executed": False, "exit_code": 0}

    command = f"tar -tzf {bundle_path} >/dev/null && {post_action}"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    return {
        "executed": True,
        "exit_code": result.returncode,
        "stderr_size": len(result.stderr),
    }


def build_delivery_headers(operator: str) -> Dict[str, str]:
    return {
        "X-Operator": operator,
        "X-Delivery-User": "support-uploader",
        "X-Delivery-Password": "CaseSync!2026",
    }


def simulate_delivery(bundle_path: Path, headers: Dict[str, str]) -> Dict[str, object]:
    return {
        "bundle": str(bundle_path),
        "headers_sent": sorted(headers.keys()),
        "accepted": bundle_path.exists() and bool(headers.get("X-Delivery-Password")),
    }


def summarize(session: DeliverySession, post_result: Dict[str, object], delivery: Dict[str, object]) -> str:
    payload = {
        "case_id": session.case_id,
        "operator": session.operator,
        "channel": session.channel,
        "file_count": len(session.collected),
        "bundle": str(session.bundle_path) if session.bundle_path else None,
        "manifest": str(session.manifest_path) if session.manifest_path else None,
        "post_action": post_result,
        "delivery": delivery,
    }
    return json.dumps(payload, indent=2)


ensure_layout()

session = DeliverySession.from_env()

if not session.case_id:
    print(json.dumps({"error": "missing case_id"}, indent=2))
else:
    folder = case_folder(session.case_id)
    if not folder.exists():
        print(json.dumps({"error": "case not found"}, indent=2))
    else:
        chosen = gather_case_files(folder, session.include)
        if not chosen:
            print(json.dumps({"error": "no files selected"}, indent=2))
        else:
            staging = prepare_staging_area(session.case_id)
            session.collected = copy_selected_files(chosen, staging)
            session.manifest_path = write_manifest(session, staging)

            outbox = safe_channel_folder(session.channel)
            session.bundle_path = build_bundle(session, staging, outbox)

            post_result = run_post_action(session.bundle_path, session.post_action)
            headers = build_delivery_headers(session.operator)
            delivery = simulate_delivery(session.bundle_path, headers)

            print(summarize(session, post_result, delivery))