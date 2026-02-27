from flask import request
import subprocess

def init(app):

        @app.route('/media/probe', methods=['POST'])
        def probe_media():
                path = request.form.get("src", "")
                if not path:
                        path = ""

                src = path.strip()

                cmd = f"ffprobe -v error \"{src}\""
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = p.communicate()

                return out + err