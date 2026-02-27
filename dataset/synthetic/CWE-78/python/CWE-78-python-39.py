from flask import request as req
import subprocess

def init(app):

        @app.route('/win/proc/find', methods=['POST'])
        def find_process():
                name = req.form.get("name", "")
                if not name:
                        name = ""

                term = name.strip()

                cmd = f"Get-Process | Where-Object {{$_.Name -like '*{term}*'}} | Select-Object -First 3"
                args = ["powershell", "-NoProfile", "-Command", cmd]

                p = subprocess.run(args, capture_output=True, encoding="utf-8")
                return (p.stdout or "") + (p.stderr or "")