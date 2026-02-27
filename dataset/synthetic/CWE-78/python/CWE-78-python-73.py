from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")

def init(app):

        @app.route("/net/ping", methods=["POST"])
        def ping():
                h = (request.headers.get("X-Host") or "").strip()
                if not h or h.startswith("-") or not _RX.fullmatch(h):
                        h = "127.0.0.1"
                proc = subprocess.run(["ping", "-c", "1", h], shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout