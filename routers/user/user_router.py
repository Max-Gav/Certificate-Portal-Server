from fastapi import APIRouter, Request, Response, status
from models.user_route_models.user import User
from routers.user.service import UserService

router = APIRouter(prefix="/users")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(request: Request, response: Response, user: User):
    await UserService().login_user(response=response, user=user)

    return {"message": "Successfully logged in."}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, response: Response, user: User):
    await UserService().register_user(response=response, user=user)

    return {"message": "Successfully created an user."}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    UserService().logout_user(response=response)

    return {"message": "Successfully logged out the user."}