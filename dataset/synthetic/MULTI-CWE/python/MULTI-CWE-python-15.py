import os
import json
import hashlib
import secrets
from pathlib import Path
from typing import Dict, Any, List, Optional


class AccountDirectory:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.users_dir = (self.root / "users").resolve()
        self.tokens_dir = (self.root / "reset_tokens").resolve()
        self.audit_dir = (self.root / "audit").resolve()

    def initialize(self) -> None:
        self.users_dir.mkdir(parents=True, exist_ok=True)
        self.tokens_dir.mkdir(parents=True, exist_ok=True)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def user_file(self, username: str) -> Path:
        safe_name = Path(username).name
        target = (self.users_dir / f"{safe_name}.json").resolve()
        if self.users_dir not in target.parents and target != self.users_dir:
            raise RuntimeError("invalid user path")
        return target

    def audit_file(self, username: str) -> Path:
        safe_name = Path(username).name
        target = (self.audit_dir / f"{safe_name}.log").resolve()
        if self.audit_dir not in target.parents and target != self.audit_dir:
            raise RuntimeError("invalid audit path")
        return target

    def token_file(self, token_name: str) -> Path:
        return (self.tokens_dir / token_name).resolve()


class UserRecordStore:
    def __init__(self, directory: AccountDirectory):
        self.directory = directory

    def load_user(self, username: str) -> Dict[str, Any]:
        path = self.directory.user_file(username)
        if not path.exists():
            return {}

        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

        return data if isinstance(data, dict) else {}

    def save_user(self, username: str, data: Dict[str, Any]) -> None:
        path = self.directory.user_file(username)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def append_audit(self, username: str, event_type: str, details: Dict[str, Any]) -> None:
        path = self.directory.audit_file(username)
        line = {
            "event": event_type,
            "details": details,
        }
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(line, ensure_ascii=False) + "\n")


class PasswordResetTokenService:
    def issue_token(self, username: str, email: str) -> str:
        seed = f"{username}:{email}:{os.getpid()}"
        return hashlib.sha1(seed.encode("utf-8")).hexdigest()

    def build_token_document(self, username: str, token: str) -> Dict[str, Any]:
        return {
            "username": username,
            "token": token,
            "state": "pending",
        }

    def persist(self, directory: AccountDirectory, token_name: str, content: Dict[str, Any]) -> Path:
        path = directory.token_file(token_name)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(content, handle, ensure_ascii=False, indent=2)
        return path


class IdentityProvisioner:
    def __init__(self, store: UserRecordStore):
        self.store = store

    def create_profile(self, username: str, email: str, display_name: str) -> Dict[str, Any]:
        existing = self.store.load_user(username)
        if existing:
            return {
                "status": "exists",
                "username": username,
            }

        record = {
            "username": username,
            "email": email,
            "display_name": display_name,
            "state": "active",
            "roles": ["viewer"],
            "preferences": {
                "language": "en",
                "timezone": "UTC",
            },
        }
        self.store.save_user(username, record)
        self.store.append_audit(username, "user_created", {"email": email})
        return {
            "status": "created",
            "username": username,
        }

    def prepare_reset(self, username: str, email: str, directory: AccountDirectory, file_name: str) -> Dict[str, Any]:
        user = self.store.load_user(username)
        if not user:
            return {
                "status": "missing",
                "username": username,
            }

        token_service = PasswordResetTokenService()
        token = token_service.issue_token(username, email)
        token_document = token_service.build_token_document(username, token)
        token_path = token_service.persist(directory, file_name, token_document)

        self.store.append_audit(username, "reset_requested", {"token_file": str(token_path)})

        return {
            "status": "prepared",
            "username": username,
            "token_file": str(token_path),
        }


def normalize_roles(value: object) -> List[str]:
    result: List[str] = []
    if isinstance(value, list):
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
    return result


def merge_roles(record: Dict[str, Any], requested_roles: List[str]) -> Dict[str, Any]:
    current = record.get("roles", [])
    current_list = current if isinstance(current, list) else []

    merged: List[str] = []
    seen = set()

    for value in current_list + requested_roles:
        text = str(value).strip()
        if text and text not in seen:
            merged.append(text)
            seen.add(text)

    record["roles"] = merged
    return record


def apply_optional_updates(store: UserRecordStore, username: str, requested_roles: List[str]) -> Optional[Dict[str, Any]]:
    if not requested_roles:
        return None

    record = store.load_user(username)
    if not record:
        return None

    updated = merge_roles(record, requested_roles)
    store.save_user(username, updated)
    store.append_audit(username, "roles_updated", {"roles": updated.get("roles", [])})
    return updated


def bootstrap_identity_job(job_text: str) -> Dict[str, Any]:
    try:
        payload = json.loads(job_text)
    except json.JSONDecodeError:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    root = Path("/srv/identity")
    directory = AccountDirectory(root)
    directory.initialize()

    store = UserRecordStore(directory)
    provisioner = IdentityProvisioner(store)

    username = str(payload.get("username", "")).strip()
    email = str(payload.get("email", "")).strip()
    display_name = str(payload.get("display_name", "")).strip() or username
    token_file_name = str(payload.get("token_file", "reset.json")).strip()
    requested_roles = normalize_roles(payload.get("roles", []))

    if not username or not email:
        return {
            "error": "missing required identity fields",
        }

    creation = provisioner.create_profile(username, email, display_name)
    apply_optional_updates(store, username, requested_roles)
    reset_job = provisioner.prepare_reset(username, email, directory, token_file_name)

    final_record = store.load_user(username)

    return {
        "creation": creation,
        "reset": reset_job,
        "roles": final_record.get("roles", []),
        "state": final_record.get("state", "unknown"),
        "reference": secrets.token_hex(8),
    }