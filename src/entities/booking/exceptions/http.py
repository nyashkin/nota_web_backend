from fastapi import status

from src.core.exceptions.http import BaseHTTPException


class BookingsNotFoundHTTPException(BaseHTTPException):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "Bookings not found",
            None,
        )
