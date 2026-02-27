from flask import request
import subprocess

def _build(tool: str, value: str) -> str:
        return f"{tool} {value}"

def init(app):

        @app.route('/tools/net', methods=['POST'])
        def net_tool():
                op = request.form.get("op", "")
                arg = request.form.get("arg", "")
                if not op:
                        op = ""
                if not arg:
                        arg = ""

                tool = op.strip().lower()
                value = arg.strip()

                cmd = _build(tool, value)
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr