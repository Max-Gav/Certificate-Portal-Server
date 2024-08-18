import os
import time
from fastapi import HTTPException, Request, Response, status
import jwt

from models.common.token_payload import TokenPayload
from settings import Settings
from jwt.exceptions import DecodeError

# .env variables/ Constants
settings = Settings()
JWT_ALGORITHM = settings.jwt_algorithm
JWT_SECRET = os.getenv("JWT_SECRET")
EXPIRY_TIME_MINUTES = 30
EXPIRY_TIME = EXPIRY_TIME_MINUTES * 60  # Seconds


# Class that provides access token utilities for creating, encoding, etc.
class AccessTokenUtils:
    # Access token payload middleware
    def __call__(self, request: Request) -> TokenPayload:
        try:
            payload = AccessTokenUtils.get_access_token_payload(request=request)

            if payload is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Access token not found")
            return payload
        except DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is invalid")

    # Build an access token payload
    @staticmethod
    def __access_token_payload_builder(user_id: str, user_role: str) -> TokenPayload:
        return TokenPayload(
            id=user_id,
            role=user_role,
            expiry=time.time() + EXPIRY_TIME
        )

    # Decode an access token
    @staticmethod
    def __decode_access_token(token: str):
        decoded_token = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token

    # Get the access token according to the client type
    @staticmethod
    def __get_access_token_from_cookies(request: Request) -> str:
        return request.cookies.get('access-token')

    # Create a new token
    @staticmethod
    def create_access_token(user_id: str, user_role: str) -> str:
        payload = AccessTokenUtils.__access_token_payload_builder(user_id, user_role)
        token = jwt.encode(payload=dict(payload), key=JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    # Return the access token data
    @staticmethod
    def get_access_token_payload(request: Request) -> TokenPayload | None:
        access_token = AccessTokenUtils.__get_access_token_from_cookies(request)

        if access_token is None:
            return None

        payload = AccessTokenUtils.__decode_access_token(token=access_token)
        return payload

    # Set the access token in the response cookies
    @staticmethod
    def set_access_token_in_cookies(response: Response, access_token: str) -> None:
        response.set_cookie(key='access-token', value=access_token, httponly=True, secure=True, samesite='none',
                            max_age=EXPIRY_TIME)

    # Remove the access token from the cookies
    @staticmethod
    def remove_access_token_from_cookies(response: Response) -> None:
        response.delete_cookie(key='access-token', httponly=True, secure=True, samesite='none')
