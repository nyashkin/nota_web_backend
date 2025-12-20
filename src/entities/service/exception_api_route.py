from typing import Any, Callable, Coroutine

from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from src.entities.service.exceptions.domain import (
    NotUniqueServiceTitleError,
    ServiceCategoryForServiceNotFoundError,
    ServiceNotFoundError,
)
from src.entities.service.exceptions.http import (
    NotUniqueServiceTitleHTTPException,
    ServiceCategoryForServiceNotFoundHTTPException,
    ServiceNotFoundHTTPException,
)


class ServiceExceptionHandlerRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        orig_handle = super().get_route_handler()

        async def service_exception_handler(resp: Request) -> Response:
            try:
                return await orig_handle(resp)
            except ServiceNotFoundError:
                raise ServiceNotFoundHTTPException
            except NotUniqueServiceTitleError:
                raise NotUniqueServiceTitleHTTPException
            except ServiceCategoryForServiceNotFoundError as e:
                raise ServiceCategoryForServiceNotFoundHTTPException(
                    e.service_category_id,
                )
            except Exception as e:
                logger.error(e)
                raise

        return service_exception_handler
