from flask import Flask, request, abort

app = Flask(__name__)

DATA_HOME = "/srv/app/notes"


@app.route("/note", methods=["GET"])
def read_note():
    note_name = request.args.get("name", "")
    if not note_name:
        abort(400)

    file_path = DATA_HOME + "/" + note_name
    with open(file_path, "r", encoding="utf-8") as fh:
        return fh.read()