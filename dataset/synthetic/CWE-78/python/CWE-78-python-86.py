from flask import request
import configparser
import subprocess

def init(app):

        @app.route("/sys/show", methods=["POST"])
        def show():
                raw = request.form.get("v") or ""

                conf = configparser.ConfigParser()
                conf.add_section("s")
                conf.set("s", "a", "fixed")
                conf.set("s", "b", raw)

                val = conf.get("s", "a")

                proc = subprocess.run(["sh", "-c", "echo \"$1\"", "_", val],
                                   shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout