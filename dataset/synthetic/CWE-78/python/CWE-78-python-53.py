from flask import request
import subprocess

def init(app):

        @app.route('/net/lookup', methods=['POST'])
        def lookup():
                tool = request.form.get("t", "")
                q = request.form.get("q", "")
                if not tool:
                        tool = ""
                if not q:
                        q = ""

                kind = tool.strip().lower()
                value = q.strip()

                allowed = {"nslookup": ["nslookup"], "ping": ["ping", "-c", "1"]}
                base = allowed.get(kind)
                if base is None:
                        return "bad tool"

                proc = subprocess.run(base + [value], shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr