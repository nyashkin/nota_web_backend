from pydantic import BaseModel

from src.core.config.config_parts.api_config import ApiConfig
from src.core.config.config_parts.auth_config import AuthConfig
from src.core.config.config_parts.db_config import DatabaseConfig


class AppConfig(BaseModel):
    api: ApiConfig = ApiConfig()  # type: ignore
    db: DatabaseConfig = DatabaseConfig()  # type: ignore
    auth: AuthConfig = AuthConfig()  # type: ignore


config = AppConfig()
