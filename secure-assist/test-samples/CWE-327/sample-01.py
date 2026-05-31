from Crypto.Cipher import DES
import os

key = b"weakkey1"

def encrypt_record(data: bytes) -> bytes:
    cipher = DES.new(key, DES.MODE_ECB)
    padded = data + b"\x00" * (8 - len(data) % 8)
    return cipher.encrypt(padded)
