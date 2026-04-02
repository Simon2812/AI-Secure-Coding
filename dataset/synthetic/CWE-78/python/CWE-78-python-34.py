from flask import request
import subprocess

def init(app):

        @app.route('/net/ping', methods=['GET'])
        def do_ping():
                host = request.args.get("host", "")
                if not host:
                        host = ""

                target = host.strip()

                proc = subprocess.run(["ping", "-c", "1", target],
                                      shell=False,
                                      capture_output=True,
                                      encoding="utf-8")

                return proc.stdout + proc.stderr