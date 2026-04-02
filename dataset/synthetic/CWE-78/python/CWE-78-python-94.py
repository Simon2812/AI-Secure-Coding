from flask import request
import subprocess

def init(app):

        @app.route("/sys/time", methods=["GET"])
        def time():
                mode = (request.args.get("m") or "").strip().lower()
                argv = ["date"] if mode != "utc" else ["date", "-u"]

                proc = subprocess.Popen(argv, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = proc.communicate()
                return out if out else err