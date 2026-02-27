from flask import request
import subprocess

def init(app):

        @app.route('/ops/mixed', methods=['POST'])
        def mixed():
                mode = request.form.get("mode", "")
                value = request.form.get("value", "")

                if mode == "safe":
                        proc = subprocess.run(["echo", value],
                                              shell=False,
                                              capture_output=True,
                                              encoding="utf-8")
                else:
                        cmd = f"sh -c 'echo {value}'"
                        proc = subprocess.run(cmd,
                                              shell=True,
                                              capture_output=True,
                                              encoding="utf-8")

                return proc.stdout + proc.stderr