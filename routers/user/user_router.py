from fastapi import APIRouter, Request, Response, status
from models.user_models import User
from routers.user.service import UserService
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(request: Request, response: Response, user: User):
    await UserService().login_check(request, response, user)

    return JSONResponse(content={"message": "Successfully logged in."}, status_code=status.HTTP_200_OK)
