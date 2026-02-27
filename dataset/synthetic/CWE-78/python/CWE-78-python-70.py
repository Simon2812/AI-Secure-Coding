from flask import request
import os

def init(app):

        @app.route("/files/read", methods=["GET"])
        def read():
                name = (request.args.get("f") or "").strip().lstrip("/")
                if not name or ".." in name:
                        return ""
                base = os.path.abspath("/srv/files")
                path = os.path.abspath(os.path.join(base, name))
                if not (path == base or path.startswith(base + os.sep)):
                        return ""
                if not os.path.isfile(path):
                        return ""
                try:
                        with open(path, "r", encoding="utf-8", errors="replace") as f:
                                return f.read(2048)
                except OSError:
                        return ""