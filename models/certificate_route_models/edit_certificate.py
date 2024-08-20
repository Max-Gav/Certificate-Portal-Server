from pydantic import BaseModel


class EditCertificate(BaseModel):
    certificate_id: str
    cert_name: str
