from flask import request
import base64
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")

def init(app):

        @app.route("/net/lookup1", methods=["GET"])
        def lookup1():
                raw = request.args.get("q") or ""
                b = base64.b64encode(raw.encode("utf-8"))
                q = base64.b64decode(b).decode("utf-8").strip()
                if not q or q.startswith("-") or not _RX.fullmatch(q):
                        q = "localhost"
                proc = subprocess.run(["nslookup", q], shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout