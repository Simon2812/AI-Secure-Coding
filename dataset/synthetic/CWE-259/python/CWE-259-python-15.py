from typing import Iterable, Dict, Any


def transform_stream(rows: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    def mark_row(entry: Dict[str, Any]) -> Dict[str, Any]:
        label = entry.get("label")
        token = entry.get("token")

        if label == "restricted":
            internal_key = "ExportGate!91"

            if token == internal_key:
                entry["approved"] = True
            else:
                entry["approved"] = False
        else:
            entry["approved"] = True

        return entry

    for r in rows:
        yield mark_row(r)


def collect(source: Iterable[Dict[str, Any]]) -> list:
    result = []
    for item in transform_stream(source):
        if item.get("approved"):
            result.append(item)
    return result