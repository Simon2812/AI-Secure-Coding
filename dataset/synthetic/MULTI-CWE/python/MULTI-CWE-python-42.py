import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, Callable, List


def build_pipeline(root: Path) -> Callable[[str], Dict[str, Any]]:
    root = root.resolve()
    data_root = (root / "data").resolve()
    out_root = (root / "out").resolve()
    db_file = (root / "state" / "pipeline.sqlite3").resolve()

    data_root.mkdir(parents=True, exist_ok=True)
    out_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    def resolve_input(name: str) -> Path:
        part = Path(name).name
        candidate = (data_root / part).resolve()
        if data_root not in candidate.parents and candidate != data_root:
            raise RuntimeError("invalid input path")
        return candidate

    def resolve_output(name: str) -> Path:
        part = Path(name).name
        candidate = (out_root / part).resolve()
        if out_root not in candidate.parents and candidate != out_root:
            raise RuntimeError("invalid output path")
        return candidate

    def load_groups(group: str) -> List[str]:
        conn = sqlite3.connect(str(db_file))
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT target FROM pipeline_targets WHERE group_name = ?",
                (group,),
            )
            return [r[0] for r in cur.fetchall()]
        finally:
            conn.close()

    def command_builder(action: str) -> List[str]:
        mapping = {
            "scan": ["file", "-b"],
            "lines": ["wc", "-l"],
        }
        return list(mapping.get(action, mapping["scan"]))

    def stage_executor(path: Path, action: str) -> Dict[str, Any]:
        cmd = command_builder(action) + [str(path)]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        return {
            "code": proc.returncode,
            "out": len(proc.stdout),
        }

    def transform(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for item in records:
            result.append(
                {
                    "file": item["file"],
                    "status": item["execution"]["code"],
                    "size": item["execution"]["out"],
                }
            )
        return result

    def write_output(path: Path, payload: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def handler(request_text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(request_text)
        except json.JSONDecodeError:
            return {"error": "invalid"}

        group = str(payload.get("group", "")).strip()
        action = str(payload.get("action", "scan")).strip()
        input_name = str(payload.get("input", "")).strip()
        output_name = str(payload.get("output", "result.json")).strip()

        if not group or not input_name:
            return {"error": "missing fields"}

        targets = load_groups(group)
        input_path = resolve_input(input_name)

        if not input_path.exists():
            return {"error": "missing input"}

        execution = stage_executor(input_path, action)

        records = [
            {
                "file": input_path.name,
                "execution": execution,
                "targets": len(targets),
            }
        ]

        transformed = transform(records)

        output_path = resolve_output(output_name)
        write_output(
            output_path,
            {
                "count": len(transformed),
                "items": transformed,
            },
        )

        return {
            "written": str(output_path),
            "count": len(transformed),
        }

    return handler


run_pipeline = build_pipeline(Path("/srv/pipeline_runtime"))