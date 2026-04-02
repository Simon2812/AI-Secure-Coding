from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")

def init(app):

        @app.route("/net/lookup", methods=["POST"])
        def lookup():
                q = (request.form.get("q") or "").strip()
                if not q or q.startswith("-") or not _RX.fullmatch(q):
                        q = "localhost"

                out = subprocess.check_output(["nslookup", q], shell=False, encoding="utf-8", errors="replace")
                return out