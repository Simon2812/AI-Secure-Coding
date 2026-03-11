from flask import request
from helpers.utils import escape_for_html
import urllib.parse
import configparser
import pathlib
import helpers.utils


def bind_endpoints(app):

    @app.route('/snapshots/read', methods=['GET'])
    def read_snapshot_get():
        return read_snapshot_post()

    @app.route('/snapshots/read', methods=['POST'])
    def read_snapshot_post():
        status = ""

        raw = request.query_string.decode("utf-8")

        pos = raw.find("snapshot" + "=")
        if pos == -1:
            return "request.query_string did not contain expected parameter 'snapshot'."

        value = raw[pos + len("snapshot") + 1:]

        cut = value.find("&")
        if cut != -1:
            value = value[:cut]

        value = urllib.parse.unquote_plus(value)

        cfg = configparser.ConfigParser()
        cfg.add_section("runtime")
        cfg.set("runtime", "constant", "fixed")
        cfg.set("runtime", "dynamic", value)

        snapshot_name = cfg.get("runtime", "dynamic")

        try:
            root = pathlib.Path(helpers.utils.TESTFILES_DIR)
            target = root / snapshot_name

            status += (
                f"The beginning of file '{escape_for_html(str(target))}' is:\n\n"
                f"{escape_for_html(target.read_text()[:1000])}"
            )

        except OSError as err:
            status += (
                f"Problem reading from file '{escape_for_html(str(target))}': "
                f"{escape_for_html(err.strerror)}"
            )

        return status