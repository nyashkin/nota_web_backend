from collections.abc import Callable
from typing import Any, Coroutine

from fastapi import Request, Response
from fastapi.routing import APIRoute
from loguru import logger

from src.entities.booking.exceptions.domain import BookingsNotFoundError
from src.entities.booking.exceptions.http import BookingsNotFoundHTTPException
from src.entities.notary_profiles.exceptions.domain import (
    NotaryProfileIsNotUniqueError,
    NotaryProfileNotFoundError,
)
from src.entities.notary_profiles.exceptions.http import (
    NotaryProfileIsNotUniqueHTTPException,
    NotaryProfileNotFoundHTTPException,
)


class NotaryProfileExceptionApiRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        orig_route = super().get_route_handler()

        async def exception_api_route(request: Request):
            try:
                return await orig_route(request)
            except NotaryProfileNotFoundError:
                raise NotaryProfileNotFoundHTTPException
            except NotaryProfileIsNotUniqueError:
                raise NotaryProfileIsNotUniqueHTTPException
            except BookingsNotFoundError:
                raise BookingsNotFoundHTTPException
            except Exception as e:
                logger.error(e)
                raise e

        return exception_api_route
