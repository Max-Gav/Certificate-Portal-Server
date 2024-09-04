from enum import Enum


class ServiceEndpoints(Enum):
    CREATE_CERTIFICATE_ENDPOINT = "/cert-ops/create-certificate"
    UPLOAD_CERTIFICATE_ENDPOINT = "/cert-ops/upload-certificate"
