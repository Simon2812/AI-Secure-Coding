import os
from flask import Flask, request, abort

app = Flask(__name__)

asset_dir = "/data/assets"


def open_asset(name):
    location = os.path.join(asset_dir, name)
    with open(location, "rb") as handle_obj:
        return handle_obj.read()


@app.route("/asset", methods=["GET"])
def serve_asset():
    resource = request.args.get("r", "")
    if resource == "":
        abort(400)

    data = open_asset(resource)
    return data