from enum import StrEnum


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthUrls(StrEnum):
    REFRESH_URL = "/auth/refresh"
    LOGIN_URL = "/auth/login"
