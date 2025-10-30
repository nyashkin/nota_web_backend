from fastapi import APIRouter
from pydantic import PositiveInt
from starlette import status

from src.auth.dependencies import AuthRequiredDI
from src.entities.service.dependencies import ServiceServiceDI
from src.entities.service.exception_handler import ServiceExceptionHandlerRoute
from src.entities.service.exceptions.domain import (
    NotUniqueServiceTitleException,
    ServiceNotFoundException,
)
from src.entities.service.exceptions.http import (
    NotUniqueServiceTitleHTTPException,
    ServiceNotFoundHTTPException,
)
from src.entities.service.schemas import (
    ServiceCreateSchema,
    ServiceReadSchema,
    ServiceUpdateSchema,
)

services_router = APIRouter(
    prefix="/services",
    tags=["💵 Services"],
    route_class=ServiceExceptionHandlerRoute,
)


@services_router.post(
    "/", status_code=status.HTTP_201_CREATED, dependencies=[AuthRequiredDI]
)
async def create_service(
    service_service: ServiceServiceDI,
    service_create: ServiceCreateSchema,
) -> ServiceReadSchema:
    try:
        service_read = await service_service.create_service(service_create)
    except NotUniqueServiceTitleException:
        raise NotUniqueServiceTitleHTTPException
    return service_read


@services_router.get("/")
async def get_service(
    service_service: ServiceServiceDI,
    service_id: int,
) -> ServiceReadSchema:
    try:
        service_read = await service_service.get_service_by_id(service_id)
    except ServiceNotFoundException:
        raise ServiceNotFoundHTTPException
    return service_read


@services_router.patch("/", dependencies=[AuthRequiredDI])
async def update_service(
    service_service: ServiceServiceDI,
    service_id: PositiveInt,
    service_update: ServiceUpdateSchema,
) -> ServiceReadSchema:
    try:
        service_read = await service_service.update_service(
            service_id,
            service_update,
        )
    except ServiceNotFoundException:
        raise ServiceNotFoundHTTPException
    except NotUniqueServiceTitleException:
        raise NotUniqueServiceTitleHTTPException
    return service_read


@services_router.delete(
    "/",
    dependencies=[AuthRequiredDI],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    service_service: ServiceServiceDI,
    service_id: PositiveInt,
) -> None:
    await service_service.delete_service(service_id)
    return None
