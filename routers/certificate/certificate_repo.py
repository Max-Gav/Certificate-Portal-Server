from fastapi import HTTPException
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

    async def find_all_user_certificates(self, user_id: str) -> list:
        user_certificates = await self.db["certificates"].find({"user_id": user_id}).to_list(length=None)
        for certificate in user_certificates:
            self.general_utils.convert_object_id_to_str(certificate)
        return user_certificates

    # Function that creates a certificate from scratch,
    # including creating the .key and the .cert files, and adds it to the system.
    async def create_certificate_in_database(self, certificate: Certificate) -> ObjectId:
        try:
            new_certificate_details = await self.db["certificates"].insert_one(certificate.model_dump())
            return new_certificate_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificate already exists.")

    # Function that adds an already existing certificate to the system.
    async def add_certificate_in_database(self, certificate: Certificate) -> ObjectId:
        try:
            new_certificate_details = await self.db["certificates"].insert_one(certificate.model_dump())
            return new_certificate_details.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Certificate already exists.")
