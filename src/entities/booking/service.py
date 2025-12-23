from src.core.database.dependencies import UoWDI
from src.entities.booking.exceptions.domain import BookingsNotFoundError
from src.entities.booking.schemas import BookingCreateSchema, BookingReadSchema


class BookingService:
    def __init__(
        self,
        uow: UoWDI,
    ) -> None:
        self._uow = uow

    async def create_booking(
        self,
        booking_create_schema: BookingCreateSchema,
    ) -> BookingReadSchema:
        booking_schema = await self._uow.booking_repository.create_booking(
            booking_create_schema
        )
        return booking_schema

    async def get_bookings_by_id(
        self,
        id: int,
    ) -> list[BookingReadSchema]:
        booking_schemas = await self._uow.booking_repository.get_bookings_by_id(id)
        if not booking_schemas:
            raise BookingsNotFoundError
        return booking_schemas

    async def get_booking_by_customer_profile_id(
        self,
        customer_profile_id: int,
    ) -> list[BookingReadSchema]:
        booking_schemas = (
            await self._uow.booking_repository.get_bookings_by_customer_profile_id(
                customer_profile_id
            )
        )
        if not booking_schemas:
            raise BookingsNotFoundError
        return booking_schemas

    async def get_booking_by_notary_profile_id(
        self,
        notary_profile_id: int,
    ) -> list[BookingReadSchema]:
        booking_schemas = (
            await self._uow.booking_repository.get_bookings_by_notary_profile_id(
                notary_profile_id
            )
        )
        if not booking_schemas:
            raise BookingsNotFoundError
        return booking_schemas
