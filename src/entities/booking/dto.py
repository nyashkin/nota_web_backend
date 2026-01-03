from decimal import Decimal

from pydantic import PositiveInt

from src.core.dto import BaseDTO


class BookingCreateDTO(BaseDTO):
    service_id: PositiveInt
    notary_profile_id: PositiveInt
    customer_profile_id: PositiveInt
    commission_percent: Decimal
    commission_amount: Decimal
    total_amount: Decimal
