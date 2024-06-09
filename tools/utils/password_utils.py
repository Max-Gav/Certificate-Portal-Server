import os
import aiobcrypt
import base64


# Class that provides password utilities for checking, encoding, etc.
class PasswordUtils:
    pepper_secret = os.getenv("PEPPER_SECRET")

    # Check password length
    def is_password_length_valid(self, password: str):
        return 8 <= len(password) <= 20

    # Decode password from base64
    def decode_password_from_base64(self, password):
        return base64.b64decode(password).decode('utf-8')

    # Encrypt a password using hash from base64
    async def encrypt_base64_password(self, password: str) -> str:
        decoded_password = self.decode_password_from_base64(password)

        peppered_password = decoded_password + self.pepper_secret
        salt = await aiobcrypt.gensalt()
        hashed_password = await aiobcrypt.hashpw(peppered_password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    # Check if the provided password matches the hashed password
    async def compare_password(self, password: str, hashed_password: str) -> bool:
        decoded_password = self.decode_password_from_base64(password)
        peppered_password = decoded_password + self.pepper_secret

        return await aiobcrypt.checkpw(peppered_password.encode('utf-8'), hashed_password.encode('utf-8'))

