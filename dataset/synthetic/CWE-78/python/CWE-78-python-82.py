from flask import request
import subprocess
import os
import re

_RX = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")

def init(app):

        @app.route("/repo/branch1", methods=["POST"])
        def branch1():
                name = (request.form.get("p") or "").strip()
                if not name or not _RX.fullmatch(name):
                        return ""

                base = os.path.abspath("/srv/projects")
                cwd = os.path.abspath(os.path.join(base, name))

                if not (cwd == base or cwd.startswith(base + os.sep)):
                        return ""
                if not os.path.isdir(cwd):
                        return ""

                p = subprocess.run(["git", "branch"], cwd=cwd, shell=False,
                                   capture_output=True, encoding="utf-8")
                return p.stdout