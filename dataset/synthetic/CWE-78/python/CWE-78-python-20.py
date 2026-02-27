from flask import request
import subprocess

def init(app):

        @app.route('/media/thumb', methods=['POST'])
        def make_thumb():
                src = request.form.get("src", "")
                size = request.form.get("size", "128")
                if not src:
                        src = ""
                if not size:
                        size = "128"

                w = size.strip()
                path = src.strip()

                cmd = f"ffmpeg -y -i {path} -vf scale={w}:-1 thumb.jpg"
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = p.communicate()

                return out + err