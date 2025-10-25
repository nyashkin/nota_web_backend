from src.core.exceptions.domain import BaseDomainException


class PasswordOrUsernameInvalidException(BaseDomainException):
    def __str__(self) -> str:
        return "Username or password is invalid"


class InvalidJwtTokenException(BaseDomainException):
    def __str__(self) -> str:
        return "Invalid jwt token"


class JwtTokenExpiredException(BaseDomainException):
    def __str__(self) -> str:
        return "Jwt token expired"


class JwtInvalidTokenTypeException(BaseDomainException):
    def __init__(self, type: str):
        self.type = type

    def __str__(self) -> str:
        return f"Invalid token type {self.type}"
