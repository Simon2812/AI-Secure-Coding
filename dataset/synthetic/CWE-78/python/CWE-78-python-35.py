from flask import request
import subprocess

def init(app):

        @app.route('/sys/info', methods=['GET'])
        def sys_info():
                name = request.args.get("name", "")
                if not name:
                        name = ""

                cmd = f"echo '{name}'"
                p = subprocess.run(cmd, shell=True,
                                      capture_output=True,
                                      encoding="utf-8")

                return p.stdout + p.stderr