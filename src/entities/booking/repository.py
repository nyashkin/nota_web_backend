from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.booking.models import BookingOrm
from src.entities.booking.schemas import BookingCreateSchema, BookingReadSchema


class BookingRepository:
    def __init__(self, _session: AsyncSession):
        self._session = _session

    async def create_booking(
        self,
        booking_create_schema: BookingCreateSchema,
    ) -> BookingReadSchema:
        booking_orm = BookingOrm(**booking_create_schema.model_dump())
        self._session.add(booking_orm)
        await self._session.flush()
        await self._session.refresh(booking_orm)
        return BookingReadSchema.model_validate(booking_orm)

    async def get_bookings_by_id(
        self,
        id: int,
    ) -> list[BookingReadSchema]:
        query = select(BookingOrm).where(BookingOrm.id == id)
        query_result = await self._session.execute(query)
        booking_orms = query_result.scalars()
        return [
            BookingReadSchema.model_validate(booking_orm)
            for booking_orm in booking_orms
        ]

    async def get_bookings_by_customer_profile_id(
        self,
        customer_profile_id: int,
    ) -> list[BookingReadSchema]:
        query = select(BookingOrm).where(
            BookingOrm.customer_profile_id == customer_profile_id
        )
        query_result = await self._session.execute(query)
        booking_orms = query_result.scalars()
        return [
            BookingReadSchema.model_validate(booking_orm)
            for booking_orm in booking_orms
        ]

    async def get_bookings_by_notary_profile_id(
        self,
        notary_profile_id: int,
    ) -> list[BookingReadSchema]:
        query = select(BookingOrm).where(
            BookingOrm.notary_profile_id == notary_profile_id
        )
        query_result = await self._session.execute(query)
        booking_orms = query_result.scalars()
        return [
            BookingReadSchema.model_validate(booking_orm)
            for booking_orm in booking_orms
        ]
