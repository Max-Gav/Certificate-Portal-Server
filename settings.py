from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app: str = "main:app"
    host: str = "127.0.0.1"
    port: int = 9000
    reload: bool = True
