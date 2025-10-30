from fastapi import APIRouter
from pydantic import PositiveInt
from starlette import status

from src.auth.dependencies import AuthRequiredDI
from src.entities.service_category.dependencies import ServiceCategoryServiceDI
from src.entities.service_category.exception_handler import (
    ServiceCategoryExceptionHandleRoute,
)
from src.entities.service_category.schemas import (
    ServiceCategoryCreateShema,
    ServiceCategoryReadSchema,
    ServiceCategoryUpdateShema,
)

service_categories_router = APIRouter(
    prefix="/services_categories",
    tags=["📑 Services categories"],
    route_class=ServiceCategoryExceptionHandleRoute,
)


@service_categories_router.post(
    "/",
    dependencies=[AuthRequiredDI],
    response_model=ServiceCategoryReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    create_category: ServiceCategoryCreateShema,
) -> ServiceCategoryReadSchema:
    return await service_categories_service.create_category(create_category)


@service_categories_router.get("/", response_model=list[ServiceCategoryReadSchema])
async def get_all_categories(
    service_categories_service: ServiceCategoryServiceDI,
) -> list[ServiceCategoryReadSchema]:
    return await service_categories_service.get_all()


@service_categories_router.patch(
    "/",
    dependencies=[AuthRequiredDI],
    response_model=ServiceCategoryReadSchema,
)
async def update_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: PositiveInt,
    update_category: ServiceCategoryUpdateShema,
) -> ServiceCategoryReadSchema:
    return await service_categories_service.update_category(
        category_id, update_category
    )


@service_categories_router.delete(
    "/",
    dependencies=[AuthRequiredDI],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service_category(
    service_categories_service: ServiceCategoryServiceDI,
    category_id: PositiveInt,
) -> None:
    return await service_categories_service.delete_category(category_id)
