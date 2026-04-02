from flask import request
import subprocess

def init(app):

        @app.route("/win/info", methods=["POST"])
        def info():
                key = (request.form.get("k") or "").strip().lower()
                scripts = {
                        "time": "Get-Date",
                        "me": "whoami",
                }
                script = scripts.get(key, "whoami")
                proc = subprocess.run(["powershell", "-NoProfile", "-Command", script],
                                   shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout