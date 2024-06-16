from fastapi import APIRouter, Response, status, Request

from models.common.token_payload import TokenPayload
from models.user_route_models.user import BaseUser
from routers.user.user_service import UserService

router = APIRouter(prefix="/users")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(response: Response, base_user: BaseUser):
    await UserService().login_user(response=response, base_user=base_user)

    return "Successfully logged in."


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(response: Response, base_user: BaseUser):
    await UserService().register_user(response=response, base_user=base_user)

    return "Successfully created an user."


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    UserService().logout_user(response=response)

    return "Successfully logged out the user."
