from typing import Dict, Iterable, List


def collect_visible(rows: Iterable[Dict[str, str]], supplied_key: str, expected_key: str) -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []

    for row in rows:
        scope = row.get("scope")

        if scope == "internal":
            if supplied_key == expected_key:
                result.append(row)
        else:
            result.append(row)

    return result