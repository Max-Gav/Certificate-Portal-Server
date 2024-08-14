import os

import httpx
from fastapi import HTTPException, status
from models.certificate_route_models.certificate import EditCertificate, BaseCertificate, Certificate, FullCertificate
from models.common.token_payload import TokenPayload
from routers.certificate.certificate_repo import CertificateRepo
from tools.utils.access_token_utils import AccessTokenUtils
from bson.objectid import ObjectId


class CertificateService:
    def __init__(self) -> None:
        self._repo = CertificateRepo()
        self.access_token_utils = AccessTokenUtils()
        self.certificate_operations_service_url = os.getenv(
            "CERTIFICATE_OPERATIONS_SERVICE_URL") or "http://127.0.0.1:9200"

    async def get_certificates(self, payload: TokenPayload) -> list:
        return await self._repo.get_all_certificates(payload["id"])

    async def create_certificate(self, base_certificate: BaseCertificate, payload: TokenPayload) -> None:
        certificate = Certificate(user_id=payload["id"], **(base_certificate.model_dump()))
        certificate_objectid = await self._repo.create_certificate(certificate=certificate)

        create_certificate_url = self.certificate_operations_service_url + "/cert-ops/create-certificate"

        full_certificate = FullCertificate(certificate_id=str(certificate_objectid), **(certificate.model_dump()))

        async with httpx.AsyncClient() as client:
            response = await client.post(url=create_certificate_url, data=full_certificate.model_dump_json())
            match response.status_code:
                case 201:
                    pass
                case 400:
                    raise HTTPException(status_code=400, detail=response.json().get("detail"))
                case _:
                    raise HTTPException(status_code=500, detail="Internal Server Error")

    async def add_certificate(self, base_certificate: BaseCertificate, payload: TokenPayload) -> None:
        certificate = Certificate(user_id=payload["id"], **(base_certificate.model_dump()))
        await self._repo.add_certificate(certificate=certificate)

    async def edit_certificate_details(self, edit_certificate: EditCertificate, payload: TokenPayload) -> None:
        updated_values = edit_certificate.model_dump(exclude={"certificate_id"})
        certificate_id = ObjectId(edit_certificate.certificate_id)

        edit_result = await self._repo.edit_certificate_details(certificate_id=certificate_id,
                                                                updated_values=updated_values,
                                                                user_id=payload["id"])
        if edit_result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching certificate found to "
                                                                              "edit.")

    async def delete_certificate(self, certificate_id: str, payload: TokenPayload) -> None:
        certificate_id = ObjectId(certificate_id)
        user_id = payload["id"]

        delete_user_result = await self._repo.delete_certificate(certificate_id, user_id)

        if delete_user_result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching certificate found to "
                                                                              "delete.")
