from pydantic import PositiveInt
from pydantic_settings import BaseSettings


class ServerConfig(
    BaseSettings,
    env_prefix="SERVER_",
):
    title: str
    port: PositiveInt
    host: str
    debug: bool
    cors_origins: list[str]
