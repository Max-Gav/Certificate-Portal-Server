from fastapi import HTTPException
from starlette import status

from db.db import MongoConnector
from models.user_route_models.user import User, BaseUser
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
class UserRepo:
    def __init__(self):
        self.db = MongoConnector().db

    async def find_user_in_database(self, base_user: BaseUser) -> dict:
        user_from_db = await self.db["users"].find_one({"username": base_user.username})
        return user_from_db

    async def create_user_in_database(self, user: User) -> ObjectId:
        try:
            new_user_details = await self.db["users"].insert_one(user.model_dump())
            return new_user_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already taken.")

