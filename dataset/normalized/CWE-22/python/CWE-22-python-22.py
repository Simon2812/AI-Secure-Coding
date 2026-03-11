from flask import request
from helpers.utils import escape_for_html
import configparser
import helpers.utils


def configure_routes(app):

    @app.route('/reports/save', methods=['GET'])
    def save_report_get():
        return save_report_post()

    @app.route('/reports/save', methods=['POST'])
    def save_report_post():
        result = ""

        query_value = request.args.get("report")
        if not query_value:
            query_value = ""

        cfg = configparser.ConfigParser()
        cfg.add_section("settings")
        cfg.set("settings", "fixed", "value")
        cfg.set("settings", "dynamic", query_value)

        report_name = cfg.get("settings", "dynamic")

        try:
            output_file = f"{helpers.utils.TESTFILES_DIR}/{report_name}"

            with open(output_file, "wb") as writer:
                result += (
                    f"Now ready to write to file: {escape_for_html(output_file)}"
                )

        except IOError as e:
            result += (
                f"Problem reading from file '{escape_for_html(output_file)}': "
                f"{escape_for_html(e.strerror)}"
            )

        return result