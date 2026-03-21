import hashlib


def select_hash(value):
    if not value:
        return None

    data = value.encode('utf-8')

    algo = 'sha256' if len(data) < 16 else 'sha512'
    engine = hashlib.new(algo)
    engine.update(data)

    return engine.hexdigest()


def run():
    return [
        select_hash("short"),
        select_hash("this_is_a_longer_input_value")
    ]