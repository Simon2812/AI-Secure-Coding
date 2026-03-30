import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List


TOOLS_ROOT = Path("/opt/tools").resolve()


class ToolRegistry:
    def __init__(self):
        self._tools = {
            "disk": ["df", "-h"],
            "memory": ["free", "-m"],
            "uptime": ["uptime"]
        }

    def get_base_command(self, name: str) -> List[str]:
        return self._tools.get(name, [])


class CommandBuilder:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def build(self, tool_name: str, extra: str) -> str:
        base = self.registry.get_base_command(tool_name)
        if not base:
            return ""

        base_cmd = " ".join(base)
        return f"{base_cmd} {extra}".strip()


class ExecutionService:
    def __init__(self, working_dir: Path):
        self.working_dir = working_dir

    def _ensure_dir(self):
        self.working_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, command: str) -> Dict[str, str]:
        self._ensure_dir()

        result = subprocess.run(
            command,
            shell=True,
            cwd=str(self.working_dir),
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }


class ReportFormatter:
    def format(self, tool: str, result: Dict[str, str]) -> Dict[str, object]:
        return {
            "tool": tool,
            "success": result["code"] == 0,
            "output_size": len(result["stdout"]),
            "error_size": len(result["stderr"])
        }


def load_request() -> Dict[str, str]:
    raw = os.environ.get("TOOL_REQUEST", "{}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    return {
        "tool": str(data.get("tool", "")),
        "extra": str(data.get("extra", ""))
    }


def resolve_tool_path(name: str) -> Path:
    safe_name = Path(name).name
    path = (TOOLS_ROOT / safe_name).resolve()

    if TOOLS_ROOT not in path.parents and path != TOOLS_ROOT:
        raise RuntimeError("invalid tool path")

    return path


def run_tool_flow() -> Dict[str, object]:
    request = load_request()

    registry = ToolRegistry()
    builder = CommandBuilder(registry)
    executor = ExecutionService(Path("/tmp/tool_runs"))
    formatter = ReportFormatter()

    tool_name = request.get("tool", "")
    extra = request.get("extra", "")

    if not tool_name:
        return {"error": "missing tool"}

    base_path = resolve_tool_path(tool_name)

    command = builder.build(tool_name, extra)
    if not command:
        return {"error": "unknown tool"}

    result = executor.execute(command)

    report = formatter.format(tool_name, result)
    report["binary"] = str(base_path)

    return report


def main():
    outcome = run_tool_flow()
    print(json.dumps(outcome, indent=2))


if __name__ == "__main__":
    main()