from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9_.-]{1,128}\Z")

def init(app):

        @app.route("/fs/list", methods=["POST"])
        def list():
                name = (request.form.get("d") or "").strip()
                if not name or name.startswith("-") or not _RX.fullmatch(name):
                        name = "tmp"
                path = "/var/" + name
                proc = subprocess.run(["ls", "-la", path], shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout