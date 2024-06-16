from models.certificate_route_models.certificate import BaseCertificate, Certificate
from models.common.token_payload import TokenPayload
from routers.certificate.certificate_repo import CertificateRepo
from tools.utils.access_token_utils import AccessTokenUtils


class CertificateService:
    def __init__(self) -> None:
        self._repo = CertificateRepo()
        self.access_token_utils = AccessTokenUtils()

    async def get_certificates(self, payload: TokenPayload) -> list:
        return await self._repo.find_all_user_certificates(payload["id"])

    async def create_certificate(self, base_certificate: BaseCertificate, payload: TokenPayload):
        certificate = Certificate(user_id=payload["id"], **(base_certificate.model_dump()))
        await self._repo.create_certificate_in_database(certificate=certificate)

    async def add_certificate(self, base_certificate: BaseCertificate, payload: TokenPayload):
        certificate = Certificate(user_id=payload["id"], **(base_certificate.model_dump()))
        await self._repo.add_certificate_in_database(certificate=certificate)
