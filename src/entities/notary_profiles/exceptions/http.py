from starlette import status

from src.core.exceptions.http import BaseHTTPException


class NotaryProfileNotFoundHTTPException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "Notary profile not found",
            None,
        )


class NotaryProfileIsNotUniqueHTTPException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "Notary profile is not unique",
            None,
        )
