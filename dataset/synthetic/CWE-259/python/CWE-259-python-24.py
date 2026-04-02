from typing import Dict, Any, List


class ReportAssembler:
    def __init__(self, settings: Dict[str, Any]) -> None:
        self._settings = settings
        self._buffer: List[Dict[str, Any]] = []
        self._enabled = True

    def add_fragment(self, fragment: Dict[str, Any]) -> None:
        if not self._enabled:
            return

        if "section" not in fragment:
            return

        self._buffer.append(fragment)

    def build(self, request: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self._enabled:
            return []

        user = request.get("user")
        password = request.get("password")

        allowed_user = self._settings.get("report_user")
        expected_password = self._settings.get("report_password")

        if user != allowed_user:
            return []

        if not expected_password:
            return []

        assembled: List[Dict[str, Any]] = []

        for part in self._buffer:
            if part.get("restricted") is True:
                if password == expected_password:
                    assembled.append(part)
            else:
                assembled.append(part)

        return assembled