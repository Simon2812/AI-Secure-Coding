import os
import json
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, List, Optional


WORKSPACE_ROOT = Path("/srv/package_mirror").resolve()
INDEX_FILE = WORKSPACE_ROOT / "index.json"


def load_package_index(index_file: Path) -> Dict[str, Dict[str, str]]:
    if not index_file.exists():
        return {}

    with open(index_file, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    if not isinstance(raw, dict):
        return {}

    normalized = {}
    for name, value in raw.items():
        if not isinstance(value, dict):
            continue

        normalized[name] = {
            "channel": str(value.get("channel", "stable")),
            "archive": str(value.get("archive", "")),
            "status": str(value.get("status", "unknown")),
        }
    return normalized


def load_request() -> Dict[str, object]:
    body = os.environ.get("MIRROR_REQUEST", "{}")
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def ensure_workspace() -> None:
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    (WORKSPACE_ROOT / "channels").mkdir(parents=True, exist_ok=True)
    (WORKSPACE_ROOT / "staging").mkdir(parents=True, exist_ok=True)


def list_archive_members(archive_path: Path) -> List[str]:
    if not archive_path.exists():
        return []

    names: List[str] = []
    with zipfile.ZipFile(archive_path, "r") as zf:
        for info in zf.infolist():
            if not info.is_dir():
                names.append(info.filename)
    return names


def safe_channel_root(channel_name: str) -> Path:
    allowed = {"stable", "beta", "internal"}
    selected = channel_name if channel_name in allowed else "stable"
    root = (WORKSPACE_ROOT / "channels" / selected).resolve()

    if WORKSPACE_ROOT not in root.parents and root != WORKSPACE_ROOT:
        raise RuntimeError("invalid channel root")

    root.mkdir(parents=True, exist_ok=True)
    return root


def stage_preview_file(target_root: Path, relative_name: str, content: str) -> Path:
    preview_dir = (target_root / "preview").resolve()
    if target_root not in preview_dir.parents and preview_dir != target_root:
        raise RuntimeError("invalid preview directory")

    preview_dir.mkdir(parents=True, exist_ok=True)
    target = (preview_dir / Path(relative_name).name).resolve()

    if preview_dir not in target.parents and target != preview_dir:
        raise RuntimeError("invalid preview file")

    with open(target, "w", encoding="utf-8") as fh:
        fh.write(content)

    return target


def unpack_selected_file(archive_path: Path, member_name: str, destination_root: Path) -> Optional[Path]:
    with zipfile.ZipFile(archive_path, "r") as zf:
        names = zf.namelist()
        if member_name not in names:
            return None

        destination_root.mkdir(parents=True, exist_ok=True)
        output_path = (destination_root / member_name).resolve()

        with zf.open(member_name, "r") as src, open(output_path, "wb") as dst:
            dst.write(src.read())

        return output_path


def build_summary(package_name: str, package_info: Dict[str, str], selected_member: str, extracted_path: Optional[Path]) -> Dict[str, object]:
    return {
        "package": package_name,
        "channel": package_info.get("channel", "stable"),
        "archive": package_info.get("archive", ""),
        "selected_member": selected_member,
        "extracted": str(extracted_path) if extracted_path else None,
        "status": package_info.get("status", "unknown"),
    }


def process_package_preview() -> Dict[str, object]:
    ensure_workspace()

    index = load_package_index(INDEX_FILE)
    request_data = load_request()

    package_name = str(request_data.get("package", ""))
    selected_member = str(request_data.get("member", "README.txt"))

    package_info = index.get(package_name)
    if not package_info:
        return {"error": "package not found"}

    channel_root = safe_channel_root(package_info.get("channel", "stable"))
    archive_path = (WORKSPACE_ROOT / "archives" / package_info.get("archive", "")).resolve()

    available_members = list_archive_members(archive_path)
    if not available_members:
        return {"error": "archive empty"}

    staging_root = Path(tempfile.mkdtemp(prefix="mirror_", dir=str(WORKSPACE_ROOT / "staging"))).resolve()
    extracted_path = unpack_selected_file(archive_path, selected_member, staging_root)

    if extracted_path is None:
        preview_text = "requested member was not present in archive"
        note_file = stage_preview_file(channel_root, f"{package_name}.txt", preview_text)
        result = build_summary(package_name, package_info, selected_member, None)
        result["note"] = str(note_file)
        result["available_count"] = len(available_members)
        return result

    with open(extracted_path, "rb") as fh:
        preview = fh.read(200)

    note_file = stage_preview_file(
        channel_root,
        f"{package_name}.txt",
        f"Preview bytes: {preview[:80].hex()}",
    )

    result = build_summary(package_name, package_info, selected_member, extracted_path)
    result["note"] = str(note_file)
    result["available_count"] = len(available_members)
    return result


def main() -> None:
    outcome = process_package_preview()
    print(json.dumps(outcome, indent=2))


if __name__ == "__main__":
    main()