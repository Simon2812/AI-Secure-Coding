import os
from flask import Flask, request, abort

app = Flask(__name__)

records_home = "/srv/internal/reports"


@app.route("/report", methods=["GET"])
def fetch_report():
    selection = request.args.get("id", "")
    if selection == "":
        abort(400)

    target_path = os.path.join(records_home, selection)

    with open(target_path, "r", encoding="utf-8") as stream:
        return stream.read()