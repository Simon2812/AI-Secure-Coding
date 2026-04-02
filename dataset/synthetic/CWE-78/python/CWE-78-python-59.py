from flask import Blueprint, request, jsonify
import subprocess
import logging
import os
from datetime import datetime

archive_bp = Blueprint("archive", name)
logger = logging.getLogger("archive_service")


def _validate_level(level: str) -> str:
        if level not in {"1", "5", "9"}:
                return "5"
        return level


def _build_archive_command(target_dir: str, level: str) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        output_name = f"/tmp/archive_{timestamp}.tar.gz"
        return f"tar -czf {output_name} -C {target_dir} . --gzip -{level}"


@archive_bp.route("/archive/create", methods=["POST"])
def create_archive():
        payload = request.get_json(silent=True) or {}

        directory = payload.get("dir", "")
        compression = payload.get("level", "5")

        if not directory:
                return jsonify({"error": "Missing directory"}), 400

        compression = _validate_level(str(compression))

        logger.info("Archive requested for %s", directory)

        if not os.path.isdir(directory):
                return jsonify({"error": "Directory not found"}), 404

        cmd = _build_archive_command(directory.strip(), compression)

        proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                encoding="utf-8"
        )

        if proc.returncode != 0:
                logger.error("Archive failed: %s", proc.stderr)
                return jsonify({"error": "Archive failed"}), 500

        return jsonify({"status": "ok", "stdout": proc.stdout})