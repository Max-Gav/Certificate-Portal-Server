from fastapi import APIRouter, Request, Response, status
from models.user_models import User
from routers.user.service import UserService
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(request: Request, response: Response, user: User):
    await UserService().login_check(response=response, user=user)

    return JSONResponse(content={"message": "Successfully logged in."}, status_code=status.HTTP_200_OK)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, response: Response, user: User):
    await UserService().user_registration(response=response, user=user)

    return JSONResponse(content={"message": "Successfully created an user."}, status_code=status.HTTP_201_CREATED)

