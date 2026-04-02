from flask import request
import subprocess

def init(app):

        @app.route("/ops/cluster", methods=["GET"])
        def cluster():
                what = (request.args.get("w") or "").strip().lower()

                table = {
                        "nodes": ["kubectl", "get", "nodes"],
                        "pods": ["kubectl", "get", "pods"],
                }
                argv = table.get(what, ["kubectl", "get", "pods"])

                proc = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout