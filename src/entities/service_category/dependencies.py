from typing import Annotated

from fastapi import Depends

from src.entities.service_category.services import ServiceCategoryService

ServiceCategoryServiceDI = Annotated[
    ServiceCategoryService, Depends(ServiceCategoryService)
]
