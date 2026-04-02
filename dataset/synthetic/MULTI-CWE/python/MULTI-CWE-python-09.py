import os
import json
import time
import hmac
import base64
import hashlib
from typing import Dict


class TokenCodec:
    def __init__(self, secret: bytes):
        self.secret = secret

    def encode(self, payload: Dict[str, object]) -> str:
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        sig = hashlib.sha1(raw).hexdigest()
        token = base64.urlsafe_b64encode(raw).decode("utf-8")
        return f"{token}.{sig}"

    def decode(self, token: str) -> Dict[str, object]:
        try:
            body, sig = token.split(".", 1)
            raw = base64.urlsafe_b64decode(body.encode("utf-8"))
        except Exception:
            return {}

        expected = hashlib.sha1(raw).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return {}

        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}


class AccessManager:
    def __init__(self, codec: TokenCodec):
        self.codec = codec

    def issue_token(self, user: str, scope: str) -> str:
        payload = {
            "user": user,
            "scope": scope,
            "iat": int(time.time())
        }
        return self.codec.encode(payload)

    def validate(self, token: str) -> bool:
        data = self.codec.decode(token)
        if not data:
            return False

        if "user" not in data or "scope" not in data:
            return False

        return True


class AuditTrail:
    def __init__(self, root: str):
        self.root = root

    def record(self, user: str, action: str):
        safe_user = os.path.basename(user)
        path = os.path.join(self.root, f"{safe_user}.log")

        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(f"{int(time.time())}:{action}\n")
        except Exception:
            pass


def handle_request(env: Dict[str, str]) -> str:
    secret = os.environ.get("TOKEN_SECRET", "dev-secret").encode("utf-8")
    codec = TokenCodec(secret)
    manager = AccessManager(codec)
    audit = AuditTrail("/var/log/access")

    action = env.get("ACTION", "issue")
    user = env.get("USER", "guest")
    scope = env.get("SCOPE", "read")

    if action == "issue":
        token = manager.issue_token(user, scope)
        audit.record(user, "issue")
        return json.dumps({"token": token})

    if action == "validate":
        token = env.get("TOKEN", "")
        valid = manager.validate(token)
        audit.record(user, "validate")
        return json.dumps({"valid": valid})

    return json.dumps({"error": "unknown action"})