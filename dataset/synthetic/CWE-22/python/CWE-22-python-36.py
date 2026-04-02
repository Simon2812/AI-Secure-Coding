import os
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

workspace = "/srv/workspace/files"


@app.route("/api/file/read", methods=["POST"])
def read_file():
    payload = request.get_json(silent=True)
    if payload is None or "path" not in payload:
        abort(400)

    requested = payload["path"]

    source_file = os.path.join(workspace, requested)

    with open(source_file, "r", encoding="utf-8") as fp:
        content = fp.read()

    return jsonify({"content": content})