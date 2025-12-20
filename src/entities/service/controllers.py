from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import PositiveInt
from starlette import status

from src.auth.dependencies import AdminRoleRequiredDI
from src.entities.service.dependencies import ServiceServiceDI
from src.entities.service.exception_api_route import ServiceExceptionHandlerRoute
from src.entities.service.exceptions.domain import (
    NotUniqueServiceTitleError,
    ServiceNotFoundError,
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

# CREATE


@services_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[AdminRoleRequiredDI],
)
async def create_service(
    service_service: ServiceServiceDI,
    service_create: ServiceCreateSchema,
) -> ServiceReadSchema:
    service_read_dto = await service_service.create_service(service_create)
    return ServiceReadSchema.model_validate(service_read_dto)


# READ


@services_router.get("/{service_id}")
async def get_service(
    service_service: ServiceServiceDI,
    service_id: Annotated[PositiveInt, Path()],
) -> ServiceReadSchema:
    service_read_dto = await service_service.get_service_by_id(service_id)
    return ServiceReadSchema.model_validate(service_read_dto)


# UPDATE


@services_router.patch(
    "/{service_id}",
    dependencies=[AdminRoleRequiredDI],
)
async def update_service(
    service_service: ServiceServiceDI,
    service_id: Annotated[PositiveInt, Path()],
    service_update: ServiceUpdateSchema,
) -> ServiceReadSchema:
    try:
        service_read_dto = await service_service.update_service(
            service_id,
            service_update,
        )
    except ServiceNotFoundError:
        raise ServiceNotFoundHTTPException
    except NotUniqueServiceTitleError:
        raise NotUniqueServiceTitleHTTPException
    return ServiceReadSchema.model_validate(service_read_dto)


# DELETE


@services_router.delete(
    "/{service_id}",
    dependencies=[AdminRoleRequiredDI],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    service_service: ServiceServiceDI,
    service_id: Annotated[PositiveInt, Path()],
) -> None:
    await service_service.delete_service(service_id)
    return None
