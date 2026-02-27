from flask import request
import os
import subprocess

def init(app):

        @app.route('/win/env/echo', methods=['POST'])
        def win_env_echo():
                v = request.form.get("v", "")
                if not v:
                        v = ""

                os.environ["ECHO_VALUE"] = v.strip()

                chain = ["cmd.exe", "/c", "echo %ECHO_VALUE%"]
                p = subprocess.run(chain, capture_output=True, encoding="utf-8")

                return p.stdout + p.stderr