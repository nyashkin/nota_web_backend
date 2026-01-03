from typing import Self

import jwt
from pydantic import PositiveInt, ValidationError, model_validator
from pydantic_settings import BaseSettings


class AuthConfig(
    BaseSettings,
    env_prefix="AUTH_",
):
    access_token_expire_hours: PositiveInt
    refresh_token_expire_days: PositiveInt
    private_key: str
    public_key: str
    algorithm: str = "RS256"

    @model_validator(mode="after")
    def keys_validator(self) -> Self:
        some_payload = {"some": "payload"}

        try:
            jwt_encoded: str = jwt.encode(
                payload=some_payload,
                key=self.private_key,
                algorithm=self.algorithm,
            )
            jwt.decode(jwt_encoded, key=self.public_key, algorithms=[self.algorithm])

        except Exception:
            raise ValidationError("Private or public key is invalid")
        return self
