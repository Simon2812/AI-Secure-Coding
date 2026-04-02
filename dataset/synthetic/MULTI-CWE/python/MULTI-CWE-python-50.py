import os
import json
from pathlib import Path
from typing import Dict, Any, List


class SecretVault:
    def init(self, root: Path):
        self.root = root.resolve()

    def fetch(self, name: str) -> str:
        env_name = f"VAULT_{name.upper()}"
        env_val = os.environ.get(env_name)
        if env_val:
            return env_val

        file_part = Path(name).name
        candidate = (self.root / f"{file_part}.secret").resolve()

        if self.root not in candidate.parents and candidate != self.root:
            return ""

        if not candidate.exists():
            return ""

        try:
            return candidate.read_text(encoding="utf-8").strip()
        except OSError:
            return ""


class KeyAssembler:
    def build(self, parts: List[str]) -> str:
        combined = []
        for p in parts:
            if p:
                combined.append(p[::-1])
        return "-".join(combined)


class FileArea:
    def init(self, root: Path):
        self.root = root.resolve()

    def place(self, name: str) -> Path:
        part = Path(name).name
        target = (self.root / part).resolve()

        if self.root not in target.parents and target != self.root:
            raise RuntimeError("invalid location")

        return target


def _parse(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def run_vault_job(text: str):
    base = Path("/srv/vault_system")
    secret_root = base / "secrets"
    output_root = base / "output"

    secret_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    payload = _parse(text)

    keys = payload.get("keys")
    if not isinstance(keys, list):
        return 0

    vault = SecretVault(secret_root)

    collected: List[str] = []
    for k in keys:
        name = str(k).strip()
        if not name:
            continue
        collected.append(vault.fetch(name))

    if not collected:
        return 0

    assembled = KeyAssembler().build(collected)

    filename = str(payload.get("file", "bundle.txt")).strip()
    target = FileArea(output_root).place(filename)

    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(assembled)

    return len(assembled)
