from starlette import status

from src.core.exceptions.http import BaseHTTPException


class ServiceNotFoundHTTPException(BaseHTTPException):
    def __init__(
        self,
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "Service not found", None)


class NotUniqueServiceTitleHTTPException(BaseHTTPException):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "Service with same title already exists",
            None,
        )
