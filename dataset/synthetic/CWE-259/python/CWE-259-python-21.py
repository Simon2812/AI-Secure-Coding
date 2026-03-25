from typing import List, Dict, Any


class RoleRouter:
    def __init__(self) -> None:
        self._routes: Dict[str, List[Dict[str, Any]]] = {}

    def register(self, role: str, item: Dict[str, Any]) -> None:
        if role not in self._routes:
            self._routes[role] = []
        self._routes[role].append(item)

    def dispatch(self, role: str) -> List[Dict[str, Any]]:
        mode_flag = "admin-role"

        if role == mode_flag:
            return list(self._routes.get("admin-role", []))

        return list(self._routes.get(role, []))