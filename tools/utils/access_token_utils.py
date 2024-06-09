import os
import time
from fastapi import HTTPException, Request, Response, status
import jwt
from settings import Settings

# .env variables
settings = Settings()
JWT_ALGORITHM = settings.jwt_algorithm
JWT_SECRET = os.getenv("JWT_SECRET")

# Class that provides access token utilities for creating, encoding, etc.
class AccessTokenUtils:
    # Build a access token payload
    def access_token_payload_builder(self, user_id: str, user_role: str, expiry_time: int):
        return {
            "id": user_id,
            "role": user_role,
            "expiry": time.time() + expiry_time
        }

    # Create a new token
    def create_access_token(self, user_id: str, user_role: str) -> str:
        payload = self.access_token_payload_builder(user_id, user_role, 600)
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
        # try:
        access_token = self.get_access_token_from_cookies(request)

        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail={"Error": "Access token not found"})

        decoded_access_token = self.decode_access_token(token=access_token)
        return decoded_access_token

    # Set the access token in the response cookies
    def set_access_token_in_cookies(self, response: Response, access_token: str):
        response.set_cookie(key='access-token', value=access_token, max_age=6000)
