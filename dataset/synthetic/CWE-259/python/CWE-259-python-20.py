from typing import List, Dict, Any


def annotate_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []

    for e in events:
        label = e.get("label", "")
        token_hint = e.get("token_hint", "")

        if "password" in label.lower():
            e["category"] = "sensitive-label"
        elif token_hint.startswith("auth_"):
            e["category"] = "token-like"
        else:
            e["category"] = "normal"

        result.append(e)

    return result