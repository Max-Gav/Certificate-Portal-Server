from typing import Optional, Tuple

import httpx
from fastapi import HTTPException, status, BackgroundTasks, UploadFile
from httpx import Response
from models.certificate_route_models.upload_certificate import UploadCertificate
from models.certificate_route_models.edit_certificate import EditCertificate
from models.certificate_route_models.certificate import CertificateData, CertificateDataUserId, FullCertificateData
from models.common.token_payload import TokenPayload
from routers.certificate.certificate_repo import CertificateRepo
from tools.utils.access_token_utils import AccessTokenUtils
from bson.objectid import ObjectId
from config.api_routes import APIRoutes
from settings import settings


async def send_request_to_create_certificate(create_certificate_url: str, certificate_data_json: str):
    response: Response = await httpx.AsyncClient().post(url=create_certificate_url, data=certificate_data_json)

    if response.status_code != 200:
        print("Unexpected error occurred creating a certificate using the external service: \n" +
              response.content.decode("utf-8"))


async def send_request_to_upload_certificate(upload_certificate_url: str, certificate_file_details: UploadCertificate,
                                             certificate_file_content: bytes):
    files = {"pem_file": certificate_file_content}
    response: Response = await httpx.AsyncClient().post(url=upload_certificate_url,
                                                        data=certificate_file_details.model_dump(),
                                                        files=files)

    if response.status_code != 200:
        print("Unexpected error occurred creating a certificate using the external service: \n" +
              response.content.decode("utf-8"))


class CertificateService:
    def __init__(self) -> None:
        self._repo = CertificateRepo()
        self.access_token_utils = AccessTokenUtils()
        self.certificate_operations_service_url = settings.certificate_operations_service_url

    async def get_certificates(self, payload: TokenPayload) -> list:
        return await self._repo.get_all_certificates(payload["id"])

    async def get_certificate_file(self, certificate_id, payload: TokenPayload) -> Tuple[str, Optional[bytes]]:
        result = await self._repo.get_certificate_by_id(certificate_id=certificate_id, user_id=payload["id"])

        if result is None:
            return "No File Found", None

        certificate_filename = certificate_id + ".pem"
        certificate_file_content = await self._repo.get_certificate_file_content(certificate_id)

        return certificate_filename, certificate_file_content

    async def create_certificate(self, certificate_data: CertificateData, background_tasks: BackgroundTasks,
                                 payload: TokenPayload) -> None:
        certificate_data_user_id = CertificateDataUserId(user_id=payload["id"], **(certificate_data.model_dump()))
        certificate_object_id = await self._repo.create_certificate(certificate_data_user_id=certificate_data_user_id)

        create_certificate_url = self.certificate_operations_service_url + APIRoutes.CREATE_CERTIFICATE_ROUTE

        full_certificate_data = FullCertificateData(certificate_id=str(certificate_object_id),
                                                    **(certificate_data_user_id.model_dump()))

        background_tasks.add_task(send_request_to_create_certificate,
                                  create_certificate_url,
                                  full_certificate_data.model_dump_json())

    async def upload_certificate(self, cert_name: str,
                                 certificate_file: UploadFile,
                                 background_tasks: BackgroundTasks,
                                 payload: TokenPayload) -> None:
        upload_certificate_url = self.certificate_operations_service_url + APIRoutes.UPLOAD_CERTIFICATE_ROUTE

        certificate_upload_details = UploadCertificate(user_id=payload["id"], cert_name=cert_name)
        certificate_file_content = await certificate_file.read()
        await certificate_file.close()

        background_tasks.add_task(send_request_to_upload_certificate,
                                  upload_certificate_url,
                                  certificate_upload_details,
                                  certificate_file_content)

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
        user_id = payload["id"]

        delete_user_result = await self._repo.delete_certificate(certificate_id, user_id)

        if delete_user_result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching certificate found to "
                                                                              "delete.")
