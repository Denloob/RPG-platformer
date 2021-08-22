from cryptography.fernet import Fernet


class Crypt:
    """Map encryption and decryption"""

    @staticmethod
    def create_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt(text: str, key: bytes = None):
        if key is None:
            key = Fernet.generate_key()
            return key, Fernet(key).encrypt(text.encode())
        return Fernet(key).encrypt(text.encode())

    @staticmethod
    def decrypt(text: bytes, key: bytes):
        return Fernet(key).decrypt(text).decode("utf-8")
