from flask import request
import subprocess

def init(app):

        @app.route('/admin/logs', methods=['GET'])
        def logs():
                level = request.args.get("level", "")
                if not level:
                        level = ""

                safe = level.replace(";", "")
                cmd = f"grep {safe} /var/log/syslog"

                proc = subprocess.run(cmd, shell=True,
                                      capture_output=True,
                                      encoding="utf-8")

                return proc.stdout + proc.stderr