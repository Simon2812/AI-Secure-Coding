from flask import request
import subprocess

def init(app):

        @app.route("/ops/run", methods=["GET"])
        def run():
                op = (request.args.get("op") or "").strip().lower()
                table = {"me": ["whoami"], "time": ["date"]}
                argv = table.get(op, ["whoami"])
                proc = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout