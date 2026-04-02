import os
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, Any, Iterable, List, Optional


class SnapshotRequest:
    def init(self, payload: Dict[str, Any]):
        self.environment = str(payload.get("environment", "")).strip()
        self.cluster = str(payload.get("cluster", "")).strip()
        self.action = str(payload.get("action", "status")).strip() or "status"
        self.output_name = str(payload.get("output_name", "snapshot.json")).strip() or "snapshot.json"
        self.include_nodes = payload.get("include_nodes", [])
        self.node_limit = payload.get("node_limit", 20)

    def normalized_nodes(self) -> List[str]:
        result: List[str] = []
        if isinstance(self.include_nodes, list):
            for item in self.include_nodes:
                text = str(item).strip()
                if text:
                    result.append(text)
        return result

    def bounded_limit(self) -> int:
        try:
            value = int(self.node_limit)
        except (TypeError, ValueError):
            return 20
        if value < 1:
            return 1
        if value > 100:
            return 100
        return value


class ConfigDirectory:
    def init(self, root: Path):
        self.root = root.resolve()

    def cluster_config(self, environment: str, cluster: str) -> Optional[Path]:
        env_part = Path(environment).name
        cluster_part = Path(cluster).name

        candidate = (self.root / env_part / f"{cluster_part}.json").resolve()
        if self.root not in candidate.parents and candidate != self.root:
            return None
        return candidate

    def load_cluster(self, environment: str, cluster: str) -> Dict[str, Any]:
        path = self.cluster_config(environment, cluster)
        if path is None or not path.exists():
            return {}

        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

        return data if isinstance(data, dict) else {}


class ClusterRepository:
    def init(self, db_file: Path):
        self.db_file = db_file

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_file))

    def fetch_nodes(self, environment: str, cluster: str, requested: List[str], limit: int) -> List[Dict[str, Any]]:
        connection = self._connect()
        try:
            cursor = connection.cursor()

            if requested:
                placeholders = ",".join("?" for _ in requested)
                statement = (
                    "SELECT node_name, role, state "
                    "FROM cluster_nodes "
                    "WHERE environment = ? AND cluster_name = ? "
                    f"AND node_name IN ({placeholders}) "
                    "ORDER BY node_name "
                    "LIMIT ?"
                )
                parameters: List[Any] = [environment, cluster, *requested, limit]
                cursor.execute(statement, tuple(parameters))
            else:
                statement = (
                    "SELECT node_name, role, state "
                    "FROM cluster_nodes "
                    "WHERE environment = ? AND cluster_name = ? "
                    "ORDER BY node_name "
                    "LIMIT ?"
                )
                cursor.execute(statement, (environment, cluster, limit))

            rows = cursor.fetchall()
            result: List[Dict[str, Any]] = []
            for row in rows:
                result.append(
                    {
                        "node_name": row[0],
                        "role": row[1],
                        "state": row[2],
                    }
                )
            return result
        finally:
            connection.close()
class CommandCatalog:
    def init(self):
        self._commands = {
            "status": ["clusterctl", "status"],
            "health": ["clusterctl", "health"],
            "summary": ["clusterctl", "summary"],
        }

    def resolve(self, action: str) -> List[str]:
        return list(self._commands.get(action, self._commands["status"]))


class SnapshotExecutor:
    def init(self, catalog: CommandCatalog):
        self.catalog = catalog

    def run(self, action: str, cluster: str) -> Dict[str, Any]:
        command = self.catalog.resolve(action) + ["--cluster", cluster]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return {
            "exit_code": completed.returncode,
            "stdout_size": len(completed.stdout),
            "stderr_size": len(completed.stderr),
        }


class SecretSource:
    def init(self, root: Path):
        self.root = root.resolve()

    def token(self, environment: str) -> str:
        env_key = os.environ.get("CLUSTER_API_TOKEN", "").strip()
        if env_key:
            return env_key

        file_name = f"{Path(environment).name}.token"
        token_file = (self.root / file_name).resolve()
        if self.root not in token_file.parents and token_file != self.root:
            return ""

        if not token_file.exists():
            return ""

        try:
            return token_file.read_text(encoding="utf-8").strip()
        except OSError:
            return ""


class SnapshotWriter:
    def init(self, root: Path):
        self.root = root.resolve()

    def target(self, name: str) -> Path:
        file_part = Path(name).name
        candidate = (self.root / file_part).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            raise RuntimeError("invalid output path")
        return candidate

    def write(self, path: Path, document: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)


def _parse_request(text: str) -> Dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _compose_snapshot(
    request: SnapshotRequest,
    cluster_config: Dict[str, Any],
    nodes: Iterable[Dict[str, Any]],
    execution: Dict[str, Any],
) -> Dict[str, Any]:
    node_rows = list(nodes)
    return {
        "environment": request.environment,
        "cluster": request.cluster,
        "action": request.action,
        "cluster_display_name": str(cluster_config.get("display_name", request.cluster)),
        "node_count": len(node_rows),
        "nodes": node_rows,
        "command": execution,
    }


def create_cluster_snapshot(request_text: str) -> Dict[str, Any]:
    root = Path("/srv/cluster_snapshot").resolve()
    config_root = (root / "configs").resolve()
    secret_root = (root / "secrets").resolve()
    output_root = (root / "outbox").resolve()
    db_file = (root / "state" / "clusters.sqlite3").resolve()

    config_root.mkdir(parents=True, exist_ok=True)
    secret_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    payload = _parse_request(request_text)
    if not payload:
        return {"error": "invalid request"}

    request = SnapshotRequest(payload)
    if not request.environment or not request.cluster:
        return {"error": "missing environment or cluster"}

    config_dir = ConfigDirectory(config_root)
    repository = ClusterRepository(db_file)
    executor = SnapshotExecutor(CommandCatalog())
    secrets = SecretSource(secret_root)
    writer = SnapshotWriter(output_root)

    cluster_config = config_dir.load_cluster(request.environment, request.cluster)
    if not cluster_config:
        return {"error": "cluster config not found"}
    token = secrets.token(request.environment)
    if not token:
        return {"error": "missing api token"}

    nodes = repository.fetch_nodes(
        request.environment,
        request.cluster,
        request.normalized_nodes(),
        request.bounded_limit(),
    )

    execution = executor.run(request.action, request.cluster)
    document = _compose_snapshot(request, cluster_config, nodes, execution)

    output_path = writer.target(request.output_name)
    writer.write(output_path, document)

    return {
        "written_file": str(output_path),
        "node_count": len(document["nodes"]),
        "action": request.action,
    }