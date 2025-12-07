from fastapi import status

from src.core.exceptions.http import BaseHTTPException
from src.entities.user.exceptions.domain import (
    UsernameAlredyExistsException,
    UserNotFoundException,
)


class UserNotFoundHTTPException(BaseHTTPException):
    def __init__(self, exc: UserNotFoundException | None = None) -> None:
        if not exc:
            super().__init__(status.HTTP_404_NOT_FOUND, "User not found", None)
            return
        super().__init__(status.HTTP_404_NOT_FOUND, str(exc), None)


class UserAlreadyExistsHTTPException(BaseHTTPException):
    def __init__(self, exc: UsernameAlredyExistsException | None = None) -> None:
        if not exc:
            super().__init__(
                status.HTTP_409_CONFLICT, "User with same name already exists", None,
            )
            return
        super().__init__(status.HTTP_409_CONFLICT, str(exc), None)
