import os


class Config:
    CERTIFICATE_OPERATIONS_SERVICE_URL = os.getenv("CERTIFICATE_OPERATIONS_SERVICE_URL", "http://127.0.0.1:9200")
    CREATE_CERTIFICATE_ENDPOINT = "/cert-ops/create-certificate"
    UPLOAD_CERTIFICATE_ENDPOINT = "/cert-ops/upload-certificate"
