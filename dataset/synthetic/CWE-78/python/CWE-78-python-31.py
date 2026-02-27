from flask import request
import subprocess

def init(app):

        @app.route('/diag/disk', methods=['GET'])
        def disk_check():
                path = request.cookies.get("path", "")
                if not path:
                        path = ""

                target = path.strip()
                cmd = "du -sh {}".format(target)
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr