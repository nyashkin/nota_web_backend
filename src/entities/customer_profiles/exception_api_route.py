from collections.abc import Callable
from typing import Any, Coroutine

from fastapi import Request, Response
from fastapi.routing import APIRoute
from loguru import logger

from src.entities.customer_profiles.exceptions.domain import (
    CustomerProfileIsNotUniqueError,
    CustomerProfileNotFoundError,
)
from src.entities.customer_profiles.exceptions.http import (
    CustomerProfileIsNotUniqueHTTPException,
    CustomerProfileNotFoundHTTPException,
)


class CustomerProfileExceptionApiRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        orig_route = super().get_route_handler()

        async def exception_api_route(request: Request):
            try:
                return await orig_route(request)
            except CustomerProfileNotFoundError:
                raise CustomerProfileNotFoundHTTPException
            except CustomerProfileIsNotUniqueError:
                raise CustomerProfileIsNotUniqueHTTPException
            except Exception as e:
                logger.error(e)
                raise e

        return exception_api_route
