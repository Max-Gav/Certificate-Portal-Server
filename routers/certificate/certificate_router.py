from typing import Annotated

from fastapi import APIRouter, status, Depends

from models.certificate_route_models.certificate import BaseCertificate
from models.common.token_payload import TokenPayload
from routers.certificate.certificate_service import CertificateService
from tools.utils.access_token_utils import AccessTokenUtils

router = APIRouter(prefix="/certificate")


@router.get("/get", status_code=status.HTTP_200_OK)
async def get_certificates(
        payload: Annotated[
            TokenPayload, Depends(AccessTokenUtils().access_token_payload_middleware)]):
    return await CertificateService().get_certificates(payload=payload)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_certificate(base_certificate: BaseCertificate,
                                  payload: Annotated[
                                      TokenPayload, Depends(AccessTokenUtils().access_token_payload_middleware)]):
    await CertificateService().create_certificate(base_certificate=base_certificate, payload=payload)
    return "Created user certificate."


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_user_certificate(base_certificate: BaseCertificate,
                               payload: Annotated[
                                   TokenPayload, Depends(AccessTokenUtils().access_token_payload_middleware)]):
    await CertificateService().add_certificate(base_certificate=base_certificate, payload=payload)
    return "Added user certificate."
