import hashlib
import random
import string

class PasswordUtil:

    @staticmethod
    def hash(password: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(password.encode('utf-8'))
        hashed_password = hasher.hexdigest()
        return hashed_password
    

    @staticmethod
    def generate_password(length=12) -> str:
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        password = ''.join(random.choices(characters, k=length))
        return password
