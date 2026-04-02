from flask import request
import base64
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")

def init(app):

        @app.route("/net/ping", methods=["POST"])
        def ping():
                raw = request.cookies.get("h") or ""
                b = base64.b64encode(raw.encode("utf-8"))
                host = base64.b64decode(b).decode("utf-8").strip()

                if not host or host.startswith("-") or not _RX.fullmatch(host):
                        host = "127.0.0.1"

                p = subprocess.run(["ping", "-c", "1", host], shell=False,
                                   capture_output=True, encoding="utf-8")
                return p.stdout