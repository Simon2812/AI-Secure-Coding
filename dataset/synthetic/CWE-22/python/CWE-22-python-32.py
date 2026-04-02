import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)

archive_root = "/opt/service/exports"


@app.route("/download", methods=["GET"])
def download_export():
    item = request.args.get("file", "")
    if item == "":
        abort(400)

    candidate = os.path.join(archive_root, item)
    return send_file(candidate, as_attachment=True)