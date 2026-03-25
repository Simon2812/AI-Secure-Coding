from typing import List, Dict, Any


def normalize_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []

    for r in rows:
        password = r.get("password", "")

        if isinstance(password, str):
            r["password_length"] = len(password)
        else:
            r["password_length"] = 0

        cleaned.append(r)

    return cleaned