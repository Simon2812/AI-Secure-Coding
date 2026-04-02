import os
from flask import Flask, request, abort

app = Flask(__name__)

docs_base = "/srv/docs"


@app.route("/docs", methods=["GET"])
def docs():
    page = request.args.get("page", "").strip()

    files = os.listdir(docs_base)
    if page not in files:
        abort(404)

    file_path = os.path.join(docs_base, page)

    with open(file_path, "r", encoding="utf-8") as fh:
        return fh.read()