from cryptography.fernet import Fernet


class Crypt:
    """Map and Text encryption and decryption"""

    @staticmethod
    def create_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def encrypt(text: str, key: bytes = None) -> (bytes, bytes) or bytes:
        if key is None:
            key = Fernet.generate_key()
            return key, Fernet(key).encrypt(text.encode())
        return Fernet(key).encrypt(text.encode())

    @staticmethod
    def decrypt(text: bytes, key: bytes) -> str:
        return Fernet(key).decrypt(text).decode("utf-8")

    @staticmethod
    def map_encrypt(game_map: str = None, file_path: str = None, key: bytes = None,
                    save: bool = False, save_path: str = None) -> None or bytes:

        if game_map is None and file_path is None or game_map is not None and file_path is not None:
            return None
        elif game_map is not None:
            text = game_map
        elif file_path is not None:
            with open(file_path) as f:
                text = f.read()

        if key is None:
            key = Fernet.generate_key()
            return key, Fernet(key).encrypt(text.encode())

        if save_path is not None:
            file_path = save_path

        if save:
            with open(file_path, 'w') as f:  # open original file or the save_path file
                end_text = list(Fernet(key).encrypt(text.encode()).decode("utf-8"))
                for i in range(len(end_text)):
                    if i % 214 == 0:
                        end_text.insert(i, '\n')
                end_text = "".join(end_text)

                f.write(end_text)
            return None

        return Fernet(key).encrypt(text.encode())

    @staticmethod
    def map_decrypt(key: bytes, game_map: bytes = None, file_path: str = None) -> None or str:
        if game_map is None and file_path is None or game_map is not None and file_path is not None:
            return None
        elif game_map is not None:
            text = game_map
        elif file_path is not None:
            with open(file_path) as f:
                text = f.read().encode()

        return Fernet(key).decrypt(text).decode("utf-8")
