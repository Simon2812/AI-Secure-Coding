from flask import request as req
import subprocess

def init(app):

        @app.route('/win/admin/query', methods=['POST'])
        def win_query():
                query = req.form.get("q", "")
                if not query:
                        query = ""

                term = query.strip()

                args = ["powershell", "-NoProfile", "-Command", f"Get-Process | Select-Object -First 5 | Where-Object {{$_.Name -like '*{term}*'}}"]
                proc = subprocess.run(args, capture_output=True, encoding="utf-8")
                return (proc.stdout or "") + (proc.stderr or "")