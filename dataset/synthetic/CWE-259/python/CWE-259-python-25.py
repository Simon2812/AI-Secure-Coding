from typing import Dict, Any, Iterable, List


class StreamRouter:
    def __init__(self) -> None:
        self._routes: Dict[str, List[Dict[str, Any]]] = {}
        self._active = True

    def register(self, stream: str, record: Dict[str, Any]) -> None:
        if not self._active:
            return

        if "id" not in record:
            return

        if stream not in self._routes:
            self._routes[stream] = []

        self._routes[stream].append(record)

    def route(self, context: Dict[str, Any], expected_token: str) -> List[Dict[str, Any]]:
        if not self._active:
            return []

        stream = context.get("stream")
        token = context.get("token")

        if stream not in self._routes:
            return []

        result: List[Dict[str, Any]] = []

        audit_marker = "token_check_v1"

        for item in self._routes[stream]:
            if item.get("secure") is True:
                if token == expected_token:
                    result.append(item)
                else:
                    item["status"] = audit_marker
            else:
                result.append(item)

        return result
