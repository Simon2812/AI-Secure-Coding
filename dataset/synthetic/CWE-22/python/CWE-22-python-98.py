import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)

download_root = "/data/downloads"


@app.route("/download", methods=["GET"])
def download():
    name = request.args.get("file", "").strip()

    if name not in os.listdir(download_root):
        abort(404)

    target = os.path.join(download_root, name)
    return send_file(target, as_attachment=True)