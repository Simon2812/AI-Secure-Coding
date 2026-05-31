from cryptography.fernet import Fernet

FERNET_KEY = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="

def encrypt_data(data: bytes) -> bytes:
    f = Fernet(FERNET_KEY)
    return f.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    f = Fernet(FERNET_KEY)
    return f.decrypt(token)
