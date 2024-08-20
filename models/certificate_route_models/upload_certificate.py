from pydantic import BaseModel


class UploadCertificate(BaseModel):
    user_id: str
    cert_name: str
