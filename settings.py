from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    is_dev: bool = True
    app: str = "main:app"
    host: str = "127.0.0.1" if is_dev else ""
    port: int = 9000
    reload: bool = True
    allow_origins: List[str] = ["http://localhost:5173"] if is_dev else []
    allow_methods: List[str] = ["*"]
    allow_credentials: bool = True
    allow_headers: List[str] = ["*"]
    jwt_algorithm: str = "HS256"
