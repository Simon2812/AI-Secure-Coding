import os
import json
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, Any, Iterable, Iterator, List


class EventStream:
    def init(self, source: Path):
        self.source = source.resolve()

    def iterate(self) -> Iterator[Dict[str, Any]]:
        if not self.source.exists():
            return

        try:
            with open(self.source, "r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if isinstance(item, dict):
                        yield item
        except OSError:
            return


class Selector:
    def init(self, service: str, level: str):
        self.service = service
        self.level = level

    def match(self, item: Dict[str, Any]) -> bool:
        if self.service and str(item.get("service", "")) != self.service:
            return False
        if self.level and str(item.get("level", "")) != self.level:
            return False
        return True


class QueryLayer:
    def init(self, db_file: Path):
        self.db_file = db_file

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def load_tags(self, keys: Iterable[str]) -> Dict[str, str]:
        connection = self._connect()
        try:
            cursor = connection.cursor()

            keys_list = list(keys)
            if not keys_list:
                return {}

            placeholders = ",".join("?" for _ in keys_list)
            statement = f"SELECT key, tag FROM tag_map WHERE key IN ({placeholders})"

            cursor.execute(statement, tuple(keys_list))
            rows = cursor.fetchall()

            result: Dict[str, str] = {}
            for row in rows:
                result[str(row[0])] = str(row[1])
            return result
        finally:
            connection.close()


class PathMapper:
    def init(self, root: Path):
        self.root = root.resolve()

    def resolve_input(self, name: str) -> Path:
        file_part = Path(name).name
        candidate = (self.root / file_part).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            raise RuntimeError("invalid input path")
        return candidate

    def resolve_output(self, name: str) -> Path:
        file_part = Path(name).name
        candidate = (self.root / file_part).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            raise RuntimeError("invalid output path")
        return candidate


class Digestor:
    def init(self, key: bytes):
        self.key = key

    def compute(self, items: Iterable[Dict[str, Any]]) -> str:
        raw = json.dumps(list(items), separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(self.key + raw).hexdigest()


class Writer:
    def init(self, output: Path):
        self.output = output

    def write(self, data: Dict[str, Any]) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)


def _read_key(root: Path) -> bytes:
    env_val = os.environ.get("STREAM_KEY", "")
    if env_val:
        return env_val.encode("utf-8")

    file_path = (root / "keys" / "stream.key").resolve()
    if file_path.exists():
        try:
            return file_path.read_bytes().strip()
        except OSError:
            return b""

    return b""


def _collect_keys(items: Iterable[Dict[str, Any]]) -> List[str]:
    keys: List[str] = []
    for item in items:
        k = str(item.get("key", "")).strip()
        if k:
            keys.append(k)
    return keys
def run_stream_job(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/stream_engine").resolve()
    input_root = (root / "input").resolve()
    output_root = (root / "output").resolve()
    db_file = (root / "state" / "tags.sqlite3").resolve()

    input_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(request_text)
    except json.JSONDecodeError:
        return {"error": "invalid"}

    source_name = str(payload.get("source", "")).strip()
    output_name = str(payload.get("output", "stream.json")).strip()
    service = str(payload.get("service", "")).strip()
    level = str(payload.get("level", "")).strip()

    if not source_name:
        return {"error": "missing source"}

    mapper = PathMapper(input_root)
    input_path = mapper.resolve_input(source_name)

    selector = Selector(service, level)
    stream = EventStream(input_path)

    filtered: List[Dict[str, Any]] = []
    for item in stream.iterate() or []:
        if selector.match(item):
            filtered.append(item)

    tag_layer = QueryLayer(db_file)
    tag_map = tag_layer.load_tags(_collect_keys(filtered))

    enriched: List[Dict[str, Any]] = []
    for item in filtered:
        key = str(item.get("key", ""))
        enriched.append(
            {
                "key": key,
                "value": item.get("value"),
                "tag": tag_map.get(key, ""),
            }
        )

    key = _read_key(root)
    digest = Digestor(key).compute(enriched)

    output_path = PathMapper(output_root).resolve_output(output_name)
    Writer(output_path).write(
        {
            "count": len(enriched),
            "items": enriched,
            "digest": digest,
        }
    )

    return {
        "written": len(enriched),
        "file": str(output_path),
    }