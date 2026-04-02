from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9_-]{1,32}\Z")

def init(app):

        @app.route("/text/filter", methods=["POST"])
        def filter():
                needle = (request.form.get("q") or "").strip()
                if not needle or not _RX.fullmatch(needle):
                        needle = "root"

                p1 = subprocess.run(["ps", "-eo", "user,comm"], shell=False,
                                    capture_output=True, encoding="utf-8")

                p2 = subprocess.run(["grep", needle], shell=False,
                                    input=p1.stdout, capture_output=True, encoding="utf-8")

                return p2.stdout