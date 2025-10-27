from pydantic import PositiveInt
from pydantic_settings import BaseSettings


class ApiConfig(BaseSettings, env_prefix="API_"):
    title: str
    port: PositiveInt
    host: str
    debug: bool
    cors_origins: list[str]
