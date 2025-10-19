from pydantic import BaseModel

from src.core.config.config_parts.db_config import DatabaseConfig


class AppConfig(BaseModel):
    db: DatabaseConfig = DatabaseConfig()  # type: ignore


config = AppConfig()
