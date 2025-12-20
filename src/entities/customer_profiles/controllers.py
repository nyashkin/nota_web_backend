from fastapi import APIRouter, Body
from pydantic import PositiveInt
from typing_extensions import Annotated

from src.auth.dependencies import (
    CurrentUserDI,
    CustomerRoleRequiredDI,
)
from src.entities.booking.dependencies import BookingServiceDI
from src.entities.booking.schemas import BookingCreateSchema, BookingReadSchema
from src.entities.customer_profiles.dependencies import (
    CustomerProfileDI,
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


@customer_profiles_router.get(
    "/me/bookings",
    dependencies=[CustomerProfileRequiredDI],
    response_model=list[BookingReadSchema],
)
async def get_me_customer_profile_bookings(
    bookings_service: BookingServiceDI,
    current_profile: CustomerProfileDI,
) -> list[BookingReadSchema]:
    booking_schemas = await bookings_service.get_booking_by_customer_profile_id(
        current_profile.id
    )
    return booking_schemas


@customer_profiles_router.post(
    "/me/bookings",
    dependencies=[CustomerProfileRequiredDI],
    response_model=BookingReadSchema,
)
async def create_customer_profile_booking(
    bookings_service: BookingServiceDI,
    current_profile: CustomerProfileDI,
    service_id: Annotated[PositiveInt, Body()],
    notary_profile_id: Annotated[PositiveInt, Body()],
) -> BookingReadSchema:
    booking = await bookings_service.create_booking(
        BookingCreateSchema(
            customer_profile_id=current_profile.id,
            service_id=service_id,
            notary_profile_id=notary_profile_id,
        )
    )
    return booking
