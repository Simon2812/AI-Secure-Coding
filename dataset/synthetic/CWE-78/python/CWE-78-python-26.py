from flask import request
import subprocess
import os

def init(app):

        @app.route('/ops/env/run', methods=['POST'])
        def env_run():
                val = request.form.get("v", "")
                if not val:
                        val = ""

                item = val.strip()
                os.environ["RUN_TAG"] = item

                cmd = "sh -c 'echo $RUN_TAG && id'"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr