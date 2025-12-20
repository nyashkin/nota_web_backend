from typing import Any, Callable, Coroutine

from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from src.auth.exceptions.domain import (
    InvalidJwtTokenError,
    JwtTokenExpiredError,
)
from src.auth.exceptions.http import (
    InvalidJwtTokenHTTPException,
    JwtTokenExpiredHTTPException,
)
from src.entities.user.exception_handler import UserExceptionHandlerRoute


class AuthExceptionHandlerRoute(UserExceptionHandlerRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        user_exception_route = super().get_route_handler()

        async def auth_exception_route(request: Request) -> Response:
            try:
                return await user_exception_route(request)
            except JwtTokenExpiredError:
                raise JwtTokenExpiredHTTPException
            except InvalidJwtTokenError:
                raise InvalidJwtTokenHTTPException
            except Exception as e:
                logger.error(e)
                raise

        return auth_exception_route
