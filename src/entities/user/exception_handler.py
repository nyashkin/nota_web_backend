from typing import Any, Callable, Coroutine

from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from src.entities.user.exceptions.domain import (
    UsernameAlredyExistsException,
    UserNotFoundException,
)
from src.entities.user.exceptions.http import (
    UserAlreadyExistsHTTPException,
    UserNotFoundHTTPException,
)


class UserExceptionHandlerRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        orig_route = super().get_route_handler()

        async def user_exception_handler_route(request: Request) -> Response:
            try:
                return await orig_route(request)
            except UserNotFoundException:
                raise UserNotFoundHTTPException
            except UsernameAlredyExistsException:
                raise UserAlreadyExistsHTTPException
            except Exception as e:
                logger.error(e)
                raise

        return user_exception_handler_route
