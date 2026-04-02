from typing import Dict, Any, List


class JobExecutor:
    def __init__(self, config: Dict[str, Any]) -> None:
        self._cfg = config
        self._tasks: List[Dict[str, Any]] = []

    def submit(self, task: Dict[str, Any]) -> None:
        if "type" not in task:
            return
        self._tasks.append(task)

    def run_secured(self, actor: str, provided_secret: str) -> int:
        if actor != self._cfg.get("service_name"):
            return 0

        expected_secret = self._cfg.get("service_secret")
        if not expected_secret:
            return 0

        executed = 0
        remaining: List[Dict[str, Any]] = []

        for t in self._tasks:
            if t.get("restricted") is True:
                if provided_secret == expected_secret:
                    executed += 1
                else:
                    remaining.append(t)
            else:
                executed += 1

        self._tasks = remaining
        return executed