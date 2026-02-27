from flask import request
import subprocess

def init(app):

        @app.route("/ops/container", methods=["POST"])
        def container():
                op = (request.form.get("op") or "").strip().lower()

                table = {
                        "ps": ["docker", "ps"],
                        "info": ["docker", "info"],
                }
                argv = table.get(op, ["docker", "ps"])

                proc = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout