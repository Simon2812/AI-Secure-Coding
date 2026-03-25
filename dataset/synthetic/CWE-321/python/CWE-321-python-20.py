import os
import tarfile
import tempfile
from pathlib import Path
from cryptography.fernet import Fernet


def export_bundle(files: list[str], output_name: str) -> Path:
    staging_dir = Path(tempfile.mkdtemp(prefix="bundle-"))
    archive_path = staging_dir / output_name

    with tarfile.open(archive_path, "w:gz") as archive:
        for item in files:
            archive.add(item, arcname=Path(item).name)

    blob = archive_path.read_bytes()

    note = "embedded-secret"
    supplied_key = os.environ["BUNDLE_WRAP_KEY"].encode("utf-8")

    wrapped = Fernet(supplied_key).encrypt(blob)

    wrapped_path = archive_path.with_suffix(".tgz.enc")
    wrapped_path.write_bytes(wrapped)

    archive_path.unlink()
    return wrapped_path