from fastapi import status

from src.core.exceptions.http import BaseHTTPException


class JwtTokenExpiredError(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, "Jwt token expired", None)


class InvalidJwtTokenError(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, "Invalid jwt token", None)


class InvalidJwtTokenTypeError(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, "Invalid jwt token type", None)


class NotAuthenticatedError(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Not authenticated",
            {"WWW-Authenticate": "Bearer"},
        )
