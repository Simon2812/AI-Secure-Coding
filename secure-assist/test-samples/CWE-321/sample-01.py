from Crypto.Cipher import AES
import base64

SECRET_KEY = b"mysecretkey12345"

def encrypt(plaintext):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    padded = plaintext.ljust(16).encode()
    return base64.b64encode(cipher.encrypt(padded)).decode()

def decrypt(ciphertext):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(ciphertext)).decode().strip()
