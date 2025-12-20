from starlette import status

from src.core.exceptions.http import BaseHTTPException


class CustomerProfileNotFoundHTTPException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "Customer profile not found",
            None,
        )


class CustomerProfileIsNotUniqueHTTPException(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "Customer profile is not unique",
            None,
        )
