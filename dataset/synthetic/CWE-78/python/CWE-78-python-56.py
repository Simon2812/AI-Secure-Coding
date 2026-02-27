from flask import request
import os
import subprocess

def init(app):

        @app.route('/ops/env/grep', methods=['POST'])
        def env_grep():
                q = request.form.get("q", "")
                if not q:
                        q = ""

                needle = q.strip()
                os.environ["Q"] = needle

                cmd = "sh -c 'grep \"$Q\" /etc/hosts | head -n 3'"
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = p.communicate()

                return out + err