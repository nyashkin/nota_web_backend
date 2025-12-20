from typing import Any, Callable, Coroutine

from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from src.entities.service_category.exceptions.domain import (
    ParentServiceCategoryNotFoundError,
    ServiceCategoryCreateError,
    ServiceCategoryIdAndParentIdCannotBeEqualError,
    ServiceCategoryNotFoundError,
)
from src.entities.service_category.exceptions.http import (
    ParentServiceCategoryNotFoundHTTPException,
    ServiceCategoryCreateHTTPException,
    ServiceCategoryIdAndParentIdCannotBeEqualHTTPError,
    ServiceCategoryNotFoundHTTPException,
)


class ServiceCategoryExceptionHandleRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        orig_route = super().get_route_handler()

        async def service_category_exception_handle_route(request: Request) -> Response:
            try:
                return await orig_route(request)
            except ServiceCategoryNotFoundError:
                raise ServiceCategoryNotFoundHTTPException
            except ServiceCategoryCreateError:
                raise ServiceCategoryCreateHTTPException
            except ServiceCategoryIdAndParentIdCannotBeEqualError:
                raise ServiceCategoryIdAndParentIdCannotBeEqualHTTPError
            except ParentServiceCategoryNotFoundError:
                raise ParentServiceCategoryNotFoundHTTPException
            except Exception as e:
                logger.error(e)
                raise e

        return service_category_exception_handle_route
