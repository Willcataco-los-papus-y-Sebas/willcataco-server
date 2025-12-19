from pwdlib import PasswordHash

__hasher = PasswordHash.recommended()

class Hasher:
    @staticmethod
    def verify_password(text_password: str, hashed_password: str):
        return __hasher.verify(text_password, hashed_password)

    @staticmethod
    def get_password_hash(text_password: str):
        return __hasher.hash(text_password)
