from flask import Flask, request
import os

app = Flask(__name__)
DOCS_DIR = "/srv/documents"

@app.route("/view")
def view_doc():
    doc = request.args.get("name")
    full_path = os.path.join(DOCS_DIR, doc)
    with open(full_path, "r") as f:
        return f.read()
