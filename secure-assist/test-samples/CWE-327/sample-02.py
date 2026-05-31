from Crypto.Cipher import ARC4

key = b"rc4secretkey"

def encrypt_stream(data: bytes) -> bytes:
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def decrypt_stream(data: bytes) -> bytes:
    cipher = ARC4.new(key)
    return cipher.decrypt(data)
