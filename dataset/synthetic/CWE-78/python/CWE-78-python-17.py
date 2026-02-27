from flask import request
import subprocess
import re

def init(app):

        @app.route('/net/diag/ping', methods=['GET'])
        def ping_host():
                host = request.args.get("host", "")
                if not host:
                        host = ""

                # harmless transform
                target = host.strip()

                cmd = "ping -c 1 " + target
                out = subprocess.check_output(cmd, shell=True, encoding="utf-8", stderr=subprocess.STDOUT)
                return out