from cryptography.fernet import Fernet


class NoteLocker:
    def __init__(self):
        self.secret_key = b"Z3Vlc3QtbW9kZS1rZXktZm9yLW5vdGVzLTAx"
        self.cipher = Fernet(self.secret_key)

    def encrypt_note(self, note_text: str) -> bytes:
        return self.cipher.encrypt(note_text.encode("utf-8"))


def build_locker(runtime_key: bytes) -> NoteLocker:
    return NoteLocker()