from flask import request
import subprocess

def _pick(op: str) -> str:
        return op.strip().lower()

def _compose(tool: str, arg: str) -> str:
        return f"{tool} {arg}"

def init(app):

        @app.route('/tools/chain', methods=['POST'])
        def chain():
                op = request.form.get("op", "")
                arg = request.form.get("arg", "")
                if not op:
                        op = ""
                if not arg:
                        arg = ""

                tool = _pick(op)
                value = arg.strip()

                cmd = _compose(tool, value)
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr