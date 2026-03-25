import ssl
import socket
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def send_secure_packet(host: str, port: int, payload: bytes, key: bytes) -> None:
    context = ssl.create_default_context()

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            nonce = os.urandom(12)
            cipher = AESGCM(key)
            encrypted = cipher.encrypt(nonce, payload, None)

            secure_sock.sendall(nonce + encrypted)