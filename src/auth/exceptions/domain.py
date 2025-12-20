from src.core.exceptions.domain import BaseDomainError


class PasswordOrUsernameInvalidError(BaseDomainError):
    def __str__(self) -> str:
        return "Username or password is invalid"


class InvalidJwtTokenError(BaseDomainError):
    def __str__(self) -> str:
        return "Invalid jwt token"


class JwtTokenExpiredError(BaseDomainError):
    def __str__(self) -> str:
        return "Jwt token expired"


class JwtInvalidTokenTypeError(BaseDomainError):
    def __init__(self, type: str):
        self.type = type

    def __str__(self) -> str:
        return f"Invalid token type {self.type}"
