from fastapi import HTTPException
from pymongo.results import UpdateResult
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

    async def find_certificate(self, cert_id: str) -> ObjectId:
        certificate = await self.db["certificates"].find_one({"_id":  ObjectId(cert_id)})
        return certificate
    async def delete_cert(self, cert_id: str, user_id: str) :
         await self.db["certificates"].delete_one({"_id":  ObjectId(cert_id), "user_id": user_id})
         return "Successfully deleted"

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

    async def edit_certificate(self, certificate: Certificate) -> UpdateResult:
        try:
            query = {'_id': certificate.user_id}
            update = {'cert_name': certificate.user_id}
            certificate = await self.db["certificates"].update_one(query, {'$set': update})
            return certificate
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request.")