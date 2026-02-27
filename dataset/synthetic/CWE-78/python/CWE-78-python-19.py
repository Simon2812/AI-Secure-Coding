from flask import request as req
import os

def init(app):

        @app.route('/ops/log/rotate', methods=['POST'])
        def rotate_logs():
                target = req.form.get("path", "")
                if not target:
                        target = ""

                folder = target.strip()

                cmd = f"rm -rf {folder}/old_logs"
                status = os.system(cmd)

                return str(status)