from pydantic import PositiveInt, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class DatabaseConfig(
    BaseSettings,
    env_prefix="DB_",
):
    host: str
    port: PositiveInt
    name: str
    username: str
    password: SecretStr

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.name,
        )
