from flask import Blueprint, request, jsonify
import subprocess
import logging
import re

diag_bp = Blueprint("diagnostics", name)
log = logging.getLogger("diag_service")


def _is_valid_host(host: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z0-9\.-]{1,253}", host))


def _build_ping_command(host: str, count: str, timeout: str) -> str:
        return f"ping -c {count} -W {timeout} {host}"


@diag_bp.route("/diag/ping", methods=["POST"])
def run_ping():
        data = request.get_json(silent=True) or {}

        host = str(data.get("host", "")).strip()
        count = str(data.get("count", "1")).strip()
        timeout = str(data.get("timeout", "2")).strip()

        if not host:
                return jsonify({"error": "Missing host"}), 400

        if not _is_valid_host(host):
                return jsonify({"error": "Invalid host"}), 400

        if not count.isdigit():
                count = "1"

        if not timeout.isdigit():
                timeout = "2"

        log.info("Ping requested: %s", host)

        cmd = _build_ping_command(host, count, timeout)

        proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                encoding="utf-8"
        )

        return jsonify({
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr
        })