from pydantic import BaseModel
from datetime import datetime


class BaseCertificate(BaseModel):
    cert_name: str
    common_name: str
    subject_alternative_names: list[str]
    expiration_date: datetime


class Certificate(BaseCertificate):
    user_id: str


class EditCertificate(BaseModel):
    certificate_id: str
    cert_name: str
