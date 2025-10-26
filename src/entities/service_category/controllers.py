from fastapi import APIRouter
from pydantic import PositiveInt
from starlette import status

from src.entities.service_category.dependencies import ServiceCategoryServiceDI
from src.entities.service_category.exceptions.domain import (
    ServiceCategoryCreateException,
    ServiceCategoryNotFoundException,
    ServiceCategoryUknownException,
)
from src.entities.service_category.exceptions.http import (
    ServiceCategoryNameNotUniqueError,
    ServiceCategoryNotFoundError,
    ServiceCategoryUknownError,
)
from src.entities.service_category.schemas import (
    ServiceCategoryCreateShema,
    ServiceCategoryReadSchema,
    ServiceCategoryUpdateShema,
)

service_categories_router = APIRouter(
    prefix="/services_categories",
    tags=["📑 Services categories"],
)


@service_categories_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceCategoryReadSchema,
)
async def create_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    create_category: ServiceCategoryCreateShema,
) -> ServiceCategoryReadSchema:
    try:
        new_category = await service_categories_service.create_category(create_category)
    except ServiceCategoryCreateException:
        raise ServiceCategoryNameNotUniqueError
    except ServiceCategoryUknownException:
        raise ServiceCategoryUknownError
    return new_category


@service_categories_router.get("/", response_model=list[ServiceCategoryReadSchema])
async def get_all_categories(
    service_categories_service: ServiceCategoryServiceDI,
) -> list[ServiceCategoryReadSchema]:
    try:
        all_categories = await service_categories_service.get_all()
    except ServiceCategoryUknownException:
        raise ServiceCategoryUknownError
    return all_categories


@service_categories_router.patch(
    "/",
    response_model=ServiceCategoryReadSchema,
)
async def update_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: PositiveInt,
    update_category: ServiceCategoryUpdateShema,
) -> ServiceCategoryReadSchema:
    try:
        updated_category = await service_categories_service.update_category(
            category_id, update_category
        )
    except ServiceCategoryNotFoundException:
        raise ServiceCategoryNotFoundError
    except ServiceCategoryCreateException:
        raise ServiceCategoryNameNotUniqueError
    except ServiceCategoryUknownException:
        raise ServiceCategoryUknownError
    return updated_category


@service_categories_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: PositiveInt,
) -> None:
    try:
        await service_categories_service.delete_category(category_id)
    except ServiceCategoryUknownException:
        raise ServiceCategoryUknownError
    return None
