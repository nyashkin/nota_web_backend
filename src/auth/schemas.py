from src.auth.enums import TokenType
from src.core.schemas import BaseAppSchema


class AuthTokenRead(BaseAppSchema):
    access_token: str
    token_type: str = "bearer"


class TokenRead(AuthTokenRead):
    refresh_token: str


class TokenPayloadSchema(BaseAppSchema):
    sub: str
    jti: str
    iat: int
    exp: int
    nbf: int
    type: TokenType
