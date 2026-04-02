from flask import request
import subprocess

def init(app):

        @app.route("/proc/list", methods=["GET"])
        def list():
                h = (request.headers.get("X-Lines") or "5").strip()
                if not h.isdigit():
                        h = "5"
                n = max(1, min(int(h), 15))

                proc = subprocess.run(["ps", "-eo", "pid,comm"], shell=False, capture_output=True, encoding="utf-8")
                return "\n".join(proc.stdout.splitlines()[: n + 1])