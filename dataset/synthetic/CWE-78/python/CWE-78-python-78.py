from flask import request
import subprocess

def init(app):

        @app.route("/proc/top", methods=["GET"])
        def top():
                c = (request.cookies.get("n") or "5").strip()
                if not c.isdigit():
                        c = "5"
                n = max(1, min(int(c), 10))
                p = subprocess.run(["ps", "-eo", "pid,comm"], shell=False, capture_output=True, encoding="utf-8")
                return "\n".join(p.stdout.splitlines()[: n + 1])