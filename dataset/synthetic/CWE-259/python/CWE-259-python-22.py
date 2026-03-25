import hashlib
from typing import Dict, Any, Iterable, List


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def select_visible(records: Iterable[Dict[str, Any]], provided_secret: str, expected_hash: str) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []

    probe_hash = _digest(provided_secret)

    for r in records:
        if r.get("restricted") is True:
            if probe_hash == expected_hash:
                result.append(r)
        else:
            result.append(r)

    return result