from fastapi import HTTPException
from pymongo.results import UpdateResult, DeleteResult
from starlette import status

from db.db import MongoConnector
from models.certificate_route_models.certificate import Certificate
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from tools.utils.general_utils import GeneralUtils


class CertificateRepo:
    def __init__(self):
        self.db = MongoConnector().db
        self.general_utils = GeneralUtils()

    async def get_all_certificates(self, user_id: str) -> list:
        user_certificates = await self.db["certificates"].find({"user_id": user_id}).to_list(length=None)
        for certificate in user_certificates:
            self.general_utils.convert_object_id_to_str(certificate)
        return user_certificates

    async def get_one_certificate(self, cert_id: str) -> ObjectId:
        certificate = await self.db["certificates"].find_one({"_id": ObjectId(cert_id)})
        return certificate

    async def create_certificate(self, certificate: Certificate) -> ObjectId:
        try:
            new_certificate_details = await self.db["certificates"].insert_one(certificate.model_dump())
            return new_certificate_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificate already exists.")

    async def add_certificate(self, certificate: Certificate) -> ObjectId:
        try:
            new_certificate_details = await self.db["certificates"].insert_one(certificate.model_dump())
            return new_certificate_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificate already exists.")

    async def edit_certificate_details(self, certificate_id: ObjectId, updated_values: dict, user_id: str) -> UpdateResult:
        edit_result = await self.db["certificates"].update_one(
            {"_id": certificate_id, "user_id": user_id},
            {'$set': updated_values})
        return edit_result

    async def delete_certificate(self, cert_id: ObjectId, user_id: str) -> DeleteResult:
        delete_user_result = await self.db["certificates"].delete_one({"_id": cert_id, "user_id": user_id})
        return delete_user_result

