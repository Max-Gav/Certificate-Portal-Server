import os
import time
from fastapi import HTTPException, Request, Response, status
import jwt
from settings import Settings

# .env variables/ Constants
settings = Settings()
JWT_ALGORITHM = settings.jwt_algorithm
JWT_SECRET = os.getenv("JWT_SECRET")
EXPIRY_TIME_MINUTES = 10
EXPIRY_TIME = EXPIRY_TIME_MINUTES * 60  # Seconds


# Class that provides access token utilities for creating, encoding, etc.
class AccessTokenUtils:
    # Build an access token payload
    def access_token_payload_builder(self, user_id: str, user_role: str):
        return {
            "id": user_id,
            "role": user_role,
            "expiry": time.time() + EXPIRY_TIME
        }

    # Create a new token
    def create_access_token(self, user_id: str, user_role: str) -> str:
        payload = self.access_token_payload_builder(user_id, user_role)
        token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    # Decode an access token
    def decode_access_token(self, token: str):
        decoded_token = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token

    # Get the access token according to the client type
    def get_access_token_from_cookies(self, request: Request):
        return request.cookies.get('access-token')

    # Return the access token data
    def get_access_token_data(self, request: Request):
        access_token = self.get_access_token_from_cookies(request)

        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail={"Error": "Access token not found"})

        decoded_access_token = self.decode_access_token(token=access_token)
        return decoded_access_token

    # Set the access token in the response cookies
    def set_access_token_in_cookies(self, response: Response, access_token: str):
        response.set_cookie(key='access-token', value=access_token, httponly=True, secure=True, samesite='none',
                            max_age=EXPIRY_TIME)

    # Remove the access token from the cookies
    def remove_access_token_from_cookies(self, response: Response):
        response.delete_cookie(key='access-token', httponly=True, secure=True, samesite='none')