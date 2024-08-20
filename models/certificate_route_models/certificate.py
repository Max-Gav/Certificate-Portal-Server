from pydantic import BaseModel
from datetime import datetime


class CertificateMetaData(BaseModel):
    common_name: str
    country_name: str
    state_or_province_name: str
    locality_name: str
    organization_name: str
    organizational_unit_name: str
    email_address: str
    domain_names: list[str]
    ip_addresses: list[str]
    expiration_date: datetime


class CertificateData(CertificateMetaData):
    cert_name: str


class CertificateDataUserId(CertificateData):
    user_id: str


class CertificateDataCertId(CertificateData):
    certificate_id: str


class FullCertificateData(CertificateData):
    user_id: str
    certificate_id: str
