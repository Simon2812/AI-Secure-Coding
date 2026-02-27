from flask import request
import os
import subprocess

def init(app):

        @app.route('/ops/env/tool', methods=['POST'])
        def env_tool():
                v = request.form.get("v", "")
                if not v:
                        v = ""

                token = v.strip()
                os.environ["TASK_VALUE"] = token

                cmd = "sh -c 'printf %s \"$TASK_VALUE\"; echo; id'"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr