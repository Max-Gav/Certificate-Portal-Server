import os
import time
from fastapi import HTTPException, Request, Response, status
import jwt
from settings import Settings

# .env variables
settings = Settings()
JWT_ALGORITHM = settings.jwt_algorithm
JWT_SECRET = os.getenv("JWT_SECRET")


class AccessTokenUtils:
    # Create a new token
    def create_access_token(self, user_id: str, user_role: str) -> str:
        payload = {
            "id": user_id,
            "role": user_role,
            "expiry": time.time() + 600
        }
        token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    # Decode an access token
    def decode_access_token(self, token: str):
        # try:
        decoded_token = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token

    # except jwt.InvalidTokenError as error:
    #     logging.error(str(error))
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Invalid Access token"})
    # except Exception as error:
    #     logging.error(str(error))
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         detail={"Error": "Internal Server Error"})

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

    # except HTTPException as error:
    #     logging.error(str(error))
    #     raise error
    # except Exception as error:
    #     logging.error(str(error))
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         detail={"Error": "Internal Server Error"})

    # Set the access token in the response cookies
    def set_access_token_in_cookies(self, response: Response, access_token: str):
        response.set_cookie(key='access-token', value=access_token, max_age=6000)
