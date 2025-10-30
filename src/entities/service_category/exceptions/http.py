from starlette import status

from src.core.exceptions.http import BaseHTTPException


class ServiceCategoryNotFoundHTTPException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "Service category not found", None)

    pass


class ServiceCategoryCreateHTTPException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "Service category name is not unique or parent is not exists",
            None,
        )


class ServiceCategoryIdAndParentIdCannotBeEqualHTTPError(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Service category id and parent id cannot be equal exception",
            None,
        )
