from fastapi import status
from src.core.exceptions.http import BaseHTTPException
from src.entities.user.exceptions.domain import (
    UserAlredyExistsException,
    UserByUsernameNotFoundException,
    UserNotFoundException,
    UserUknownException,
)


class UserNotFoundError(BaseHTTPException):
    def __init__(self, exc: UserNotFoundException | None = None) -> None:
        if not exc:
            super().__init__(status.HTTP_404_NOT_FOUND, "User not found", None)
            return
        super().__init__(status.HTTP_404_NOT_FOUN, str(exc), None)


class UserByUsernameNotFoundError(BaseHTTPException):
    def __init__(self, exc: UserByUsernameNotFoundException | None = None):
        if not exc:
            super().__init__(status.HTTP_404_NOT_FOUND, "User not found", None)
            return
        super().__init__(status.HTTP_404_NOT_FOUN, str(exc), None)


class UserAlreadyExistsError(BaseHTTPException):
    def __init__(self, exc: UserAlredyExistsException | None = None) -> None:
        if not exc:
            super().__init__(
                status.HTTP_409_CONFLICT, "User with same name already exists", None
            )
            return
        super().__init__(status.HTTP_409_CONFLICT, str(exc), None)


class UserUknownError(BaseHTTPException):
    def __init__(self, exc: UserUknownException | None = None) -> None:
        if not exc:
            super().__init__(
                status.HTTP_503_SERVICE_UNAVAILABLE, "User uknown error", None
            )
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc), None)
