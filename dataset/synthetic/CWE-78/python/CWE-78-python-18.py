from flask import request
import subprocess

def init(app):

        @app.route('/ops/search/proc', methods=['GET'])
        def search_processes():
                term = request.args.get("q", "")
                if not term:
                        term = ""

                needle = term.strip()

                cmd = f"ps aux | grep {needle}"
                p = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return p.stdout + p.stderr