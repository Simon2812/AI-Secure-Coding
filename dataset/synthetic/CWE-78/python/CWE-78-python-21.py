from flask import request
import subprocess

def init(app):

        @app.route('/net/dns/lookup', methods=['GET'])
        def dns_lookup():
                q = request.args.get("name", "")
                if not q:
                        q = ""

                name = q.strip()

                args = ["sh", "-c", f"nslookup {name}"]
                p = subprocess.run(args, capture_output=True, encoding="utf-8")

                return p.stdout + p.stderr