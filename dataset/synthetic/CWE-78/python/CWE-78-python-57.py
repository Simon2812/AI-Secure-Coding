from flask import request
import os
import subprocess

def init(app):

        @app.route('/win/cmd/show', methods=['POST'])
        def show_value():
                x = request.form.get("x", "")
                if not x:
                        x = ""

                os.environ["SHOW"] = x.strip()

                chain = ["cmd.exe", "/c", "echo ^%SHOW^%"]
                proc = subprocess.run(chain, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr