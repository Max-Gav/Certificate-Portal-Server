from pydantic import BaseModel


class DeleteCertificate(BaseModel):
    certificate_id: str
