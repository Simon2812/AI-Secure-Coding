from flask import request
import subprocess

def init(app):

        @app.route('/audit/save', methods=['POST'])
        def save_audit():
                msg = request.form.get("msg", "")
                if not msg:
                        msg = ""

                text = msg.strip()

                cmd = f"echo {text} >> audit.log"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return proc.stdout + proc.stderr