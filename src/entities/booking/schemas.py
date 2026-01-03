from decimal import Decimal

from pydantic import PositiveInt

from src.core.schemas import BaseAppSchema
from src.entities.customer_profiles.schemas import CustomerProfileReadSchema
from src.entities.notary_profiles.schemas import NotaryProfileReadSchema
from src.entities.service.schemas import ServiceReadSchema


class BookingCreateSchema(BaseAppSchema):
    service_id: PositiveInt
    notary_profile_id: PositiveInt
    customer_profile_id: PositiveInt


class BookingReadSchema(BaseAppSchema):
    id: int
    commission_percent: Decimal
    commission_amount: Decimal
    total_amount: Decimal
    service: ServiceReadSchema
    notary_profile: NotaryProfileReadSchema
    customer_profile: CustomerProfileReadSchema
