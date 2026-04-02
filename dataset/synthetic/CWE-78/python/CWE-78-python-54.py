from flask import request
import os

def init(app):

        @app.route('/ops/cleanup/tmp', methods=['POST'])
        def cleanup_tmp():
                key = request.form.get("k", "")
                if not key:
                        key = ""

                tag = key.strip()

                cmd = "find /tmp -name \"{}*\" -delete".format(tag)
                rc = os.system(cmd)
                return str(rc)