from flask import request
import configparser
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/multi-input', methods=['GET'])
    def handle_get():
        return handle_post()

    @app.route('/multi-input', methods=['POST'])
    def handle_post():
        RESPONSE = ""

        values = request.form.getlist("input_values")
        param = ""
        if values:
            param = values[0]

        cfg = configparser.ConfigParser()
        cfg.add_section('sectionA')
        cfg.set('sectionA', 'key1', 'a_Value')
        cfg.set('sectionA', 'key2', param)

        bar = cfg.get('sectionA', 'key1')

        data = ''
        if isinstance(bar, str):
            data = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            data = bar.read(1000)

        if len(data) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.new('sha256')
        hash.update(data)

        output = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(output)}\n')
        RESPONSE += (
            f"Sensitive value '{helpers.utils.escape_for_html(data.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return RESPONSE