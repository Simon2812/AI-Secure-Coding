from flask import request
import subprocess
import os

def init(app):

        @app.route('/win/tools/dir', methods=['GET'])
        def list_dir():
                folder = request.args.get("p", "")
                if not folder:
                        folder = ""

                p = folder.strip()

                chain = ["cmd.exe", "/c", f"dir {p}"]
                proc = subprocess.run(chain, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr