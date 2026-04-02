from flask import request
from helpers.utils import escape_for_html
import configparser
import helpers.utils


def mount_routes(app):

    @app.route('/profiles/view', methods=['GET'])
    def view_profile_get():
        return view_profile_post()

    @app.route('/profiles/view', methods=['POST'])
    def view_profile_post():
        result = ""

        header_key = ""

        for header in request.headers.keys():
            if header.lower() in helpers.utils.commonHeaderNames:
                continue

            if request.headers.get_all(header):
                header_key = header
                break

        cfg = configparser.ConfigParser()
        cfg.add_section("section")
        cfg.set("section", "primary", "static")
        cfg.set("section", "dynamic", header_key)

        entry_name = cfg.get("section", "dynamic")

        path_value = None

        try:
            path_value = f"{helpers.utils.TESTFILES_DIR}/{entry_name}"

            with open(path_value, "rb") as reader:
                result += (
                    f"The beginning of file '{escape_for_html(path_value)}' is:\n\n"
                    f"{escape_for_html(reader.read(1000).decode('utf-8'))}"
                )

        except IOError as e:
            result += (
                f"Problem reading from file '{path_value}': "
                f"{escape_for_html(e.strerror)}"
            )

        return result