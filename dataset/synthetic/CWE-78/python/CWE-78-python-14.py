from flask import request as req, jsonify
import subprocess

def init(app):

        @app.route('/net/tools/fetch', methods=['POST'])
        def fetch_url():
                payload = req.get_json(silent=True) or {}
                target = payload.get("target", "")
                if not target:
                        target = ""

                cleaned = target.strip()

                cmd = f"curl -s {cleaned}"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return jsonify({"out": proc.stdout, "err": proc.stderr})