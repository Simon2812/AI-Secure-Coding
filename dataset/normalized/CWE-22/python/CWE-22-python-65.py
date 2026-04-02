from flask import request
from helpers.utils import escape_for_html
import configparser
import codecs
import helpers.utils


def load_handlers(app):

    @app.route('/letters/open', methods=['GET'])
    def letter_open_get():
        return letter_open_post()

    @app.route('/letters/open', methods=['POST'])
    def letter_open_post():
        notice = ""

        submitted_items = request.form.getlist("letter")
        primary_value = ""
        if submitted_items:
            primary_value = submitted_items[0]

        settings = configparser.ConfigParser()
        settings.add_section("storage")
        settings.set("storage", "default_name", "fixed_entry")
        settings.set("storage", "requested_name", primary_value)

        chosen_file = settings.get("storage", "default_name")

        try:
            stream = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{chosen_file}",
                "r",
                "utf-8"
            )

            notice += (
                f"Access to file: '{escape_for_html(stream.name)}' created."
            )
            notice += " And file already exists."

        except FileNotFoundError:
            notice += " But file doesn't exist yet."

        return notice