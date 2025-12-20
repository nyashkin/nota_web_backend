from fastapi import APIRouter

from src.auth.dependencies import CurrentUserDI, CustomerRoleRequiredDI
from src.entities.customer_profiles.dependencies import (
    CustomerProfileRequiredDI,
    CustomerProfileServiceDI,
)
from src.entities.customer_profiles.exception_api_route import (
    CustomerProfileExceptionApiRoute,
)
from src.entities.customer_profiles.schemas import (
    CustomerProfileCreateSchema,
    CustomerProfileReadSchema,
    CustomerProfileUpdateSchema,
)

customer_profiles_router = APIRouter(
    prefix="/customers",
    tags=["Customer profiles"],
    route_class=CustomerProfileExceptionApiRoute,
)


@customer_profiles_router.get(
    "/me",
    dependencies=[CustomerProfileRequiredDI],
    response_model=CustomerProfileReadSchema,
)
async def get_me_customer_profile(
    customer_profile_service: CustomerProfileServiceDI,
    current_user: CurrentUserDI,
) -> CustomerProfileReadSchema:
    customer_profile_dto = (
        await customer_profile_service.get_customer_profile_by_user_id(current_user.id)
    )
    return CustomerProfileReadSchema.model_validate(customer_profile_dto)


@customer_profiles_router.post(
    "/me",
    dependencies=[CustomerRoleRequiredDI],
    response_model=CustomerProfileReadSchema,
)
async def create_me_customer_profile(
    customer_profile_service: CustomerProfileServiceDI,
    current_user: CurrentUserDI,
    customer_profile_create: CustomerProfileCreateSchema,
) -> CustomerProfileReadSchema:
    customer_profile_dto = await customer_profile_service.create_customer_profile(
        user_id=current_user.id,
        customer_profile=customer_profile_create,
    )
    return CustomerProfileReadSchema.model_validate(customer_profile_dto)


@customer_profiles_router.put(
    "/me",
    dependencies=[CustomerProfileRequiredDI],
    response_model=CustomerProfileReadSchema,
)
async def update_me_customer_profile(
    customer_profile_service: CustomerProfileServiceDI,
    current_user: CurrentUserDI,
    customer_profile_update_schema: CustomerProfileUpdateSchema,
) -> CustomerProfileReadSchema:
    customer_profile_dto = (
        await customer_profile_service.update_customer_profile_by_user_id(
            current_user.id,
            customer_profile_update_schema,
        )
    )
    return CustomerProfileReadSchema.model_validate(customer_profile_dto)
