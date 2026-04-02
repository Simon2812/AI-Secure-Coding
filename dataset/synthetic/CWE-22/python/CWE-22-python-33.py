from flask import Flask, request, abort
from pathlib import Path

app = Flask(__name__)

content_root = Path("/var/app/templates")


@app.route("/template", methods=["GET"])
def load_template():
    slug = request.args.get("t", "")
    if slug == "":
        abort(400)

    location = content_root / slug
    with open(location, "r", encoding="utf-8") as reader:
        return reader.read()