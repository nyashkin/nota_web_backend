from fastapi import APIRouter
from pydantic import PositiveInt
from starlette import status

from src.entities.service.dependencies import ServiceServiceDI
from src.entities.service.schemas import (
    ServiceCreateSchema,
    ServiceReadSchema,
    ServiceUpdateSchema,
)

services_router = APIRouter(prefix="/services", tags=["Services"])


@services_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(
    service_service: ServiceServiceDI,
    service_create: ServiceCreateSchema,
) -> ServiceReadSchema:
    return await service_service.create_service(service_create)


@services_router.get("/")
async def get_service(
    service_service: ServiceServiceDI,
    service_id: int,
) -> ServiceReadSchema:
    return await service_service.get_service_by_id(service_id)


@services_router.patch("/")
async def update_service(
    service_service: ServiceServiceDI,
    service_id: PositiveInt,
    service_update: ServiceUpdateSchema,
) -> ServiceReadSchema:
    return await service_service.update_service(service_id, service_update)


@services_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_service: ServiceServiceDI,
    service_id: PositiveInt,
) -> None:
    return await service_service.delete_service(service_id)
