from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import PositiveInt
from starlette import status

from src.auth.dependencies import AdminRoleRequiredDI
from src.entities.service.schemas import ServiceReadSchema
from src.entities.service_category.dependencies import ServiceCategoryServiceDI
from src.entities.service_category.dto import (
    ServiceCategoryCreateDTO,
    ServiceCategoryUpdateDTO,
)
from src.entities.service_category.exception_handler import (
    ServiceCategoryExceptionHandleRoute,
)
from src.entities.service_category.schemas import (
    ServiceCategoryCreateSchema,
    ServiceCategoryReadSchema,
    ServiceCategoryUpdateSchema,
)

service_categories_router = APIRouter(
    prefix="/services_categories",
    tags=["📑 Services categories"],
    route_class=ServiceCategoryExceptionHandleRoute,
)


@service_categories_router.post(
    "/",
    dependencies=[AdminRoleRequiredDI],
    response_model=ServiceCategoryReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    create_category: ServiceCategoryCreateSchema,
) -> ServiceCategoryReadSchema:
    create_service_category_dto = ServiceCategoryCreateDTO.model_validate(
        create_category,
    )
    service_category_dto = await service_categories_service.create_category(
        create_service_category_dto,
    )
    return ServiceCategoryReadSchema.model_validate(service_category_dto)


@service_categories_router.get(
    "/",
    response_model=list[ServiceCategoryReadSchema],
    response_model_exclude_none=True,
)
async def get_all_categories(
    service_categories_service: ServiceCategoryServiceDI,
) -> list[ServiceCategoryReadSchema]:
    service_categories_dtos = await service_categories_service.get_all()

    service_categories: list[ServiceCategoryReadSchema] = [
        ServiceCategoryReadSchema.model_validate(dto) for dto in service_categories_dtos
    ]
    return service_categories


@service_categories_router.get(
    "/{category_id}/services",
    response_model=list[ServiceReadSchema],
)
async def get_services_in_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: Annotated[PositiveInt, Path()],
) -> list[ServiceReadSchema]:
    service_categories_dtos = (
        await service_categories_service.get_services_by_category_id(category_id)
    )

    service_categories: list[ServiceReadSchema] = [
        ServiceReadSchema.model_validate(dto) for dto in service_categories_dtos
    ]
    return service_categories


@service_categories_router.patch(
    "/{category_id}",
    dependencies=[AdminRoleRequiredDI],
    response_model=ServiceCategoryReadSchema,
)
async def update_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: Annotated[PositiveInt, Path()],
    update_category: ServiceCategoryUpdateSchema,
) -> ServiceCategoryReadSchema:
    service_category_update_dto = ServiceCategoryUpdateDTO.model_validate(
        update_category,
    )
    service_category_dto = await service_categories_service.update_category(
        category_id,
        service_category_update_dto,
    )
    return ServiceCategoryReadSchema.model_validate(service_category_dto)


@service_categories_router.delete(
    "/{category_id}",
    dependencies=[AdminRoleRequiredDI],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: Annotated[PositiveInt, Path()],
) -> None:
    return await service_categories_service.delete_category(category_id)
