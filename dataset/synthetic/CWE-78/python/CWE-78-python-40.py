from flask import request
import subprocess

def init(app):

        @app.route('/win/fs/list', methods=['GET'])
        def list_files():
                p = request.args.get("p", "")
                if not p:
                        p = ""

                path = p.strip()

                chain = ["cmd.exe", "/c", f"dir {path}"]
                proc = subprocess.run(chain, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr