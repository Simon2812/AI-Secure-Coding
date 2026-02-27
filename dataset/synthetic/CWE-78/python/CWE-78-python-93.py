from flask import request
import subprocess

def _cmd(kind: str):
        kind = (kind or "").strip().lower()
        if kind == "disk":
                return ["df", "-h"]
        if kind == "me":
                return ["whoami"]
        return ["uptime"]

def init(app):

        @app.route("/ops/run", methods=["POST"])
        def run():
                kind = request.headers.get("X-Op") or ""
                argv = _cmd(kind)
                proc = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout