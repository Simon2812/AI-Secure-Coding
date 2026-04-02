from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")

def run_cmd(argv):
        return subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")

def init(app):

        @app.route("/net/ping2", methods=["POST"])
        def ping2():
                h = (request.form.get("h") or "").strip()
                if not h or h.startswith("-") or not _RX.fullmatch(h):
                        h = "127.0.0.1"
                proc = run_cmd(["ping", "-c", "1", h])
                return proc.stdout