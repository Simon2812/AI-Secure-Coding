from flask import request
import subprocess

def init(app):

        @app.route('/tools/select', methods=['POST'])
        def select_tool():
                name = request.form.get("tool", "")
                arg = request.form.get("arg", "")
                if not name:
                        name = ""
                if not arg:
                        arg = ""

                tool = name.strip().lower()
                value = arg.strip()

                allowed = {"date": "date", "id": "id"}
                chosen = allowed.get(tool, tool)

                cmd = f"{chosen} {value}"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr