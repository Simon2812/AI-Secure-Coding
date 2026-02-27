from flask import request
import subprocess

def init(app):

        @app.route("/route/<x>", methods=["GET"])
        def route_x(x):
                parts = request.path.split("/")
                item = parts[1] if len(parts) > 1 else ""
                out = item
                out = "constant"
                p = subprocess.run(["sh", "-c", "echo \"$1\"", "_", out],
                                   shell=False, capture_output=True, encoding="utf-8")
                return p.stdout