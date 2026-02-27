from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")

def init(app):

        @app.route("/net/dns", methods=["GET"])
        def dns():
                q = (request.args.get("q") or "").strip()
                if not q or q.startswith("-") or not _RX.fullmatch(q):
                        q = "localhost"
                proc = subprocess.run(["nslookup", q], shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout