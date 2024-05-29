import logging
import os

from fastapi import HTTPException, status
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
        try:
            return base64.b64decode(password).decode('utf-8')
        except Exception as error:
            logging.error(str(error))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"Error": "Password is not using the right base64 encoding"})

    # Encrypt a password using hash
    async def encrypt_password(self, password: str) -> str:
        try:
            decoded_password = self.decode_password_from_base64(password)
            if not self.is_password_length_valid(decoded_password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "Invalid password"})

            peppered_password = decoded_password + self.pepper_secret
            salt = await aiobcrypt.gensalt()
            hashed_password = await aiobcrypt.hashpw(peppered_password.encode('utf-8'), salt)

            return hashed_password.decode('utf-8')
        except HTTPException as error:
            logging.error(str(error))
            raise error
        except Exception as error:
            logging.error(str(error))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={"Error": "Internal Server Error"})

    # Check if the provided password matches the hashed password
    async def compare_password(self, password: str, hashed_password: str) -> bool:
        try:
            decoded_password = self.decode_password_from_base64(password)
            peppered_password = decoded_password + self.pepper_secret

            return await aiobcrypt.checkpw(peppered_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except HTTPException as error:
            logging.error(str(error))
            raise error
        except Exception as error:
            logging.error(str(error))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={"Error": "Internal Server Error"})
