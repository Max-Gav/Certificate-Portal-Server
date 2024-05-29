from routers.user.repo import UserRepo
from models.user_models import User
from tools.utils.password_utils import PasswordUtils
from tools.utils.access_token_utils import AccessTokenUtils
from fastapi import Request, Response, HTTPException, status



class UserService:
    def __init__(self) -> None:
        self._repo = UserRepo()
        self.password_utils = PasswordUtils()
        self.access_token_utils = AccessTokenUtils()

    async def login_check(self, request: Request, response: Response, user: User):
        user_from_db = await self._repo.find_user_in_database(user)

        if user_from_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        is_same_password = await self.password_utils.compare_password(user.password, user_from_db.get("password"))
        if not is_same_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

        user_id = str(user_from_db.get("_id"))
        user_role = user_from_db.get("role")
        new_access_token = self.access_token_utils.create_access_token(user_id=user_id, user_role=user_role)
        self.access_token_utils.set_access_token_in_cookies(response=response, access_token=new_access_token)

        return True
