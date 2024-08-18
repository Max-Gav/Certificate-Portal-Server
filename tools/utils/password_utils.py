import os
import aiobcrypt
import base64


# Class that provides password utilities for checking, encoding, etc.
class PasswordUtils:
    pepper_secret = os.getenv("PEPPER_SECRET")

    # Decode password from base64
    @staticmethod
    def __decode_password_from_base64(password):
        return base64.b64decode(password).decode('utf-8')

    # Encrypt a password using hash from base64
    @staticmethod
    async def encrypt_base64_password(password: str) -> str:
        decoded_password = PasswordUtils.__decode_password_from_base64(password)

        peppered_password = decoded_password + PasswordUtils.pepper_secret
        salt = await aiobcrypt.gensalt()
        hashed_password = await aiobcrypt.hashpw(peppered_password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    # Check if the provided password matches the hashed password
    @staticmethod
    async def compare_password(password: str, hashed_password: str) -> bool:
        decoded_password = PasswordUtils.__decode_password_from_base64(password)
        peppered_password = decoded_password + PasswordUtils.pepper_secret

        return await aiobcrypt.checkpw(peppered_password.encode('utf-8'), hashed_password.encode('utf-8'))

