from Crypto.Cipher import Blowfish

KEY = b"blowfishkey"

def encrypt_blob(plaintext: bytes) -> bytes:
    bs = Blowfish.block_size
    plen = bs - divmod(len(plaintext), bs)[1]
    padding = bytes([plen]) * plen
    cipher = Blowfish.new(KEY, Blowfish.MODE_ECB)
    return cipher.encrypt(plaintext + padding)
