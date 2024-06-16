from pydantic import BaseModel


class TokenPayload(BaseModel):
    id: str
    role: str
    expiry: float
