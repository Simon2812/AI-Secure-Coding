from flask import request
import os

def _run(cmd: str) -> str:
        return os.popen(cmd).read()

def init(app):

        @app.route('/ops/head', methods=['GET'])
        def head_file():
                p = request.args.get("p", "")
                if not p:
                        p = ""

                path = p.strip()
                cmd = f"head -n 5 {path}"
                return _run(cmd)