from typing import Optional

from fastapi import HTTPException
from pymongo.results import UpdateResult, DeleteResult
from starlette import status

from db.db import MongoConnector
from models.certificate_route_models.certificate import CertificateDataUserId
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from tools.utils.general_utils import GeneralUtils


class CertificateRepo:
    def __init__(self):
        self.db = MongoConnector().db
        self.fs = MongoConnector().fs

    async def __find_certificate_file_id(self, certificate_id: str) -> Optional[ObjectId]:
        filename = certificate_id + ".pem"

        try:
            fs_cursor = self.fs.find({"filename": filename})
            file = (await fs_cursor.to_list(1))[0]
            await fs_cursor.close()
            return file["_id"]
        except Exception as e:
            print("An error occurred while trying to find the certificate file id")
            print(e)
            return None

    async def get_one_certificate(self, certificate_id: str, user_id: str) -> ObjectId:
        certificate = await self.db["certificates"].find_one({"_id": ObjectId(certificate_id), "user_id": user_id})
        return certificate

    async def get_all_certificates(self, user_id: str) -> list:
        user_certificates = await self.db["certificates"].find({"user_id": user_id}).to_list(length=None)
        for certificate in user_certificates:
            GeneralUtils.convert_object_id_to_str(certificate)
        return user_certificates

    async def get_certificate_file_content(self, certificate_id: str) -> Optional[bytes]:
        filename = certificate_id + ".pem"

        try:
            file = await self.fs.open_download_stream_by_name(filename=filename)
            file_content = await file.read()
            return file_content
        except Exception as e:
            print("An error occurred while trying to get the certificate file content")
            print(e)
            return None

    async def create_certificate(self, certificate_data_user_id: CertificateDataUserId) -> ObjectId:
        try:
            new_certificate_details = await self.db["certificates"].insert_one(certificate_data_user_id.model_dump())
            return new_certificate_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificate already exists.")

    async def upload_certificate(self, certificate_data_user_id: CertificateDataUserId) -> ObjectId:
        try:
            new_certificate_details = await self.db["certificates"].insert_one(certificate_data_user_id.model_dump())
            return new_certificate_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificate already exists.")

    async def edit_certificate_details(self, certificate_id: ObjectId, updated_values: dict,
                                       user_id: str) -> UpdateResult:
        edit_result = await self.db["certificates"].update_one(
            {"_id": certificate_id, "user_id": user_id},
            {'$set': updated_values})
        return edit_result

    async def delete_certificate(self, certificate_id: str, user_id: str) -> DeleteResult:
        certificate_object_id = ObjectId(certificate_id)
        delete_user_result = await self.db["certificates"].delete_one({"_id": certificate_object_id,
                                                                       "user_id": user_id})

        certificate_file_id = await self.__find_certificate_file_id(certificate_id)
        await self.fs.delete(certificate_file_id)

        return delete_user_result
