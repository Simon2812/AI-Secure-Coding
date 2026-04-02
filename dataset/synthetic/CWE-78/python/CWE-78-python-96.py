from flask import request
import os
import shutil

def init(app):

        @app.route("/export/pack", methods=["POST"])
        def pack():
                rel = (request.form.get("d") or "").strip().lstrip("/")
                if not rel or ".." in rel:
                        return ""

                base = os.path.abspath("/srv/data")
                target = os.path.abspath(os.path.join(base, rel))
                if not (target == base or target.startswith(base + os.sep)):
                        return ""
                if not os.path.isdir(target):
                        return ""

                name = os.path.basename(target.rstrip(os.sep)) or "data"
                out = shutil.make_archive(f"/tmp/{name}", "zip", root_dir=target)
                return out