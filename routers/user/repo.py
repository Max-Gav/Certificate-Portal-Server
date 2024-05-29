from db.db import MongoConnector
from models.user_models import User


class UserRepo:
    def __init__(self):
        self.db = MongoConnector().db

    async def find_user_in_database(self, user: User):
        user_from_db = await self.db["users"].find_one({"username": user.username})
        return user_from_db if user_from_db else None
