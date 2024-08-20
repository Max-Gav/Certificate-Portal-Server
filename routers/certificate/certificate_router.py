from typing import Annotated

from fastapi import APIRouter, status, Depends, BackgroundTasks

from models.certificate_route_models.certificate import CertificateData
from models.certificate_route_models.edit_certificate import EditCertificate
from models.common.token_payload import TokenPayload
from routers.certificate.certificate_service import CertificateService
from tools.utils.access_token_utils import AccessTokenUtils

router = APIRouter(prefix="/certificate")


@router.get("/get", status_code=status.HTTP_200_OK)
async def get_certificates(
        payload: Annotated[
            TokenPayload, Depends(AccessTokenUtils())]) -> list:
    return await CertificateService().get_certificates(payload=payload)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_certificate(certificate_data: CertificateData, background_tasks: BackgroundTasks,
                             payload: Annotated[
                                 TokenPayload, Depends(AccessTokenUtils())]
                             ) -> str:
    await CertificateService().create_certificate(certificate_data=certificate_data,
                                                  background_tasks=background_tasks,
                                                  payload=payload)
    return "Created user certificate."


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_certificate(base_certificate: BaseCertificate,
                          payload: Annotated[
                              TokenPayload, Depends(AccessTokenUtils())]) -> str:
    await CertificateService().add_certificate(base_certificate=base_certificate, payload=payload)
    return "Added user certificate."


@router.patch("/edit", status_code=status.HTTP_200_OK)
async def edit_certificate_details(edit_certificate: EditCertificate,
                                   payload: Annotated[
                                       TokenPayload, Depends(AccessTokenUtils())]) -> str:
    await CertificateService().edit_certificate_details(edit_certificate=edit_certificate, payload=payload)
    return "Edited user certificate."


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_certificate(certificate_id: Annotated[str, Body()],
                             payload: Annotated[
                                 TokenPayload, Depends(AccessTokenUtils())]) -> str:
    await CertificateService().delete_certificate(certificate_id, payload=payload)
    return "Deleted user certificate."
