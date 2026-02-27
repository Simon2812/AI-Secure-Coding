from flask import request
import subprocess

def init(app):

        @app.route('/ops/file/run', methods=['POST'])
        def run_from_file():
                filename = request.form.get("file", "")
                if not filename:
                        filename = ""

                with open(filename, "r", encoding="utf-8") as f:
                        command = f.read().strip()

                proc = subprocess.run(command, shell=True, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr