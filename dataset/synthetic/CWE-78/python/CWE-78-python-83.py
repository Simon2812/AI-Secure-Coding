from flask import request
import subprocess

def init(app):

        @app.route("/net/fetch", methods=["POST"])
        def fetch():
                data = request.get_json(silent=True) or {}
                src = (data.get("src") or "").strip().lower()

                table = {
                        "status": ["curl", "-fsSL", "https://example.com/status"],
                        "version": ["curl", "-fsSL", "https://example.com/version"],
                }
                argv = table.get(src, table["status"])

                proc = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout