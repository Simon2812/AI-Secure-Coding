from flask import request
import subprocess

def init(app):

        @app.route("/tool/show/<x>", methods=["POST"])
        def show_x(x):
                parts = request.path.split("/")
                value = parts[-1] if parts else ""
                tmp = "ABCD" + value + "WXYZ"
                out = tmp[0:4]

                proc = subprocess.run(["sh", "-c", "echo \"$1\"", "_", out],
                                   shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout