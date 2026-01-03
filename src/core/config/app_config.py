from pydantic import BaseModel

from src.core.config.config_parts.api_config import ApiConfig
from src.core.config.config_parts.auth_config import AuthConfig
from src.core.config.config_parts.db_config import DatabaseConfig
from src.core.config.config_parts.server_config import ServerConfig


class AppConfig(BaseModel):
    server: ServerConfig = ServerConfig()  # type: ignore
    db: DatabaseConfig = DatabaseConfig()  # type: ignore
    auth: AuthConfig = AuthConfig()  # type: ignore
    api: ApiConfig = ApiConfig()  # type: ignore


config = AppConfig()
