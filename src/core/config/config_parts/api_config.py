from pydantic import PositiveFloat
from pydantic_settings import BaseSettings


class ApiConfig(
    BaseSettings,
    env_prefix="API_",
):
    commission_percent: PositiveFloat
