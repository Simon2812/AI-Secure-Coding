from flask import request
import subprocess
import json

def init(app):

        @app.route('/api/run/config', methods=['POST'])
        def run_from_config():
                body = request.get_data(as_text=True)
                if not body:
                        body = "{}"

                config = json.loads(body)

                tool = config.get("tool", "")
                argument = config.get("arg", "")

                cmd = f"{tool} {argument}"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr