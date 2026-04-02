from flask import request
import subprocess

def init(app):

        @app.route('/ops/dual', methods=['POST'])
        def dual_exec():
                cmd = request.form.get("cmd", "")
                safe = request.form.get("safe", "")
                if not cmd:
                        cmd = ""
                if not safe:
                        safe = ""

                user_cmd = cmd.strip()
                safe_arg = safe.strip()

                good = subprocess.run(["printf", "%s", safe_arg], shell=False, capture_output=True, encoding="utf-8")

                bad_line = f"sh -c '{user_cmd}'"
                bad = subprocess.run(bad_line, shell=True, capture_output=True, encoding="utf-8")

                return good.stdout + bad.stdout + bad.stderr