from flask import request
import configparser
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/config-process', methods=['GET'])
    def route_get():
        return route_post()

    @app.route('/config-process', methods=['POST'])
    def route_post():
        RESPONSE = ""

        value = request.form.get("input_field")
        if not value:
            value = ""

        cfg = configparser.ConfigParser()
        cfg.add_section('sectionA')
        cfg.set('sectionA', 'key1', 'a-Value')
        cfg.set('sectionA', 'key2', value)

        bar = cfg.get('sectionA', 'key2')

        data = ''
        if isinstance(bar, str):
            data = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            data = bar.read(1000)

        if len(data) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.sha256()
        hash.update(data)

        res = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(res)}\n')
        RESPONSE += (
            f"Sensitive value '{helpers.utils.escape_for_html(data.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return RESPONSE