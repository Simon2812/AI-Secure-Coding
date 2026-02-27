from flask import request
import subprocess

def init(app):

        @app.route("/ops/run", methods=["GET"])
        def run():
                key = (request.cookies.get("k") or "").strip().lower()
                table = {
                        "id": ["id"],
                        "who": ["whoami"],
                        "up": ["uptime"],
                }
                argv = table.get(key, ["whoami"])

                proc = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout