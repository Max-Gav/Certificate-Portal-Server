from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app: str = "main:app"
    host: str = "127.0.0.1"
    port: int = 9000
    reload: bool = True
    allow_origins: List[str] = ["http://localhost:5173"]
    allow_methods: List[str] = ["*"]
    allow_credentials: bool = True
    allow_headers: List[str] = ["*"]
