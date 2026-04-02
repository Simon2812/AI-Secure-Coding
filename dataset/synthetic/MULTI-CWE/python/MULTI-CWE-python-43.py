import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Iterable


class RuleSet:
    def init(self, rules: Dict[str, Dict[str, Any]]):
        self.rules = rules

    def pick(self, name: str) -> Dict[str, Any]:
        return self.rules.get(name, {})


class ConfigLoader:
    def init(self, root: Path):
        self.root = root.resolve()

    def load(self, name: str) -> Dict[str, Any]:
        file_part = Path(name).name
        candidate = (self.root / file_part).resolve()

        if self.root not in candidate.parents and candidate != self.root:
            return {}

        if not candidate.exists():
            return {}

        try:
            with open(candidate, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

        return data if isinstance(data, dict) else {}


class FeatureRepository:
    def init(self, db_file: Path):
        self.db_file = db_file

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def fetch_flags(self, namespace: str) -> List[Dict[str, Any]]:
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT feature_key, enabled FROM feature_flags WHERE namespace = ?",
                (namespace,),
            )
            rows = cursor.fetchall()

            result: List[Dict[str, Any]] = []
            for row in rows:
                result.append(
                    {
                        "key": row[0],
                        "enabled": bool(row[1]),
                    }
                )
            return result
        finally:
            conn.close()


class TransformerChain:
    def init(self):
        self._steps: List = []

    def add(self, fn):
        self._steps.append(fn)
        return self

    def apply(self, items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        current = list(items)
        for step in self._steps:
            current = step(current)
        return current


class OutputSpace:
    def init(self, root: Path):
        self.root = root.resolve()

    def file(self, name: str) -> Path:
        part = Path(name).name
        candidate = (self.root / part).resolve()

        if self.root not in candidate.parents and candidate != self.root:
            raise RuntimeError("invalid output path")

        return candidate


def _filter_enabled(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [item for item in items if item.get("enabled")]


def _attach_rules(rule_set: RuleSet):
    def inner(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched: List[Dict[str, Any]] = []
        for item in items:
            rule = rule_set.pick(item["key"])
            enriched.append(
                {
                    "key": item["key"],
                    "enabled": item["enabled"],
                    "weight": int(rule.get("weight", 0)),
                }
            )
        return enriched

    return inner


def _summarize(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "key": item["key"],
            "score": item["weight"] * (1 if item["enabled"] else 0),
        }
        for item in items
    ]


def run_feature_job(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/feature_engine").resolve()
    config_root = (root / "configs").resolve()
    output_root = (root / "output").resolve()
    db_file = (root / "state" / "features.sqlite3").resolve()

    config_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(request_text)
    except json.JSONDecodeError:
        return {"error": "invalid"}
    namespace = str(payload.get("namespace", "")).strip()
    config_name = str(payload.get("config", "")).strip()
    output_name = str(payload.get("output", "features.json")).strip()

    if not namespace or not config_name:
        return {"error": "missing fields"}

    config_loader = ConfigLoader(config_root)
    config = config_loader.load(config_name)
    if not config:
        return {"error": "config missing"}

    rules = RuleSet(config.get("rules", {}))

    repo = FeatureRepository(db_file)
    flags = repo.fetch_flags(namespace)

    chain = (
        TransformerChain()
        .add(_filter_enabled)
        .add(_attach_rules(rules))
        .add(_summarize)
    )

    result = chain.apply(flags)

    out_path = OutputSpace(output_root).file(output_name)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "count": len(result),
                "items": result,
            },
            handle,
            indent=2,
        )

    return {
        "written": str(out_path),
        "count": len(result),
    }