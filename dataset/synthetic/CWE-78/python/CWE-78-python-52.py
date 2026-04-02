from flask import request
import subprocess

def init(app):

        @app.route('/backup/make', methods=['POST'])
        def make_backup():
                name = request.form.get("name", "")
                if not name:
                        name = ""

                base = name.strip()

                cmd = f"tar -czf {base}.tar.gz {base}"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr