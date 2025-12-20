from typing import Annotated

from fastapi import Depends

from src.auth.dependencies import CurrentCustomerUser
from src.entities.customer_profiles.dto import CustomerProfileReadDTO
from src.entities.customer_profiles.exceptions.domain import (
    CustomerProfileNotFoundError,
)
from src.entities.customer_profiles.exceptions.http import (
    CustomerProfileNotFoundHTTPException,
)
from src.entities.customer_profiles.service import CustomerProfileService

CustomerProfileServiceDI = Annotated[CustomerProfileService, Depends()]


async def get_customer_profile(
    customer_profile_service: CustomerProfileServiceDI,
    curren_customer_user: CurrentCustomerUser,
) -> CustomerProfileReadDTO:
    try:
        return await customer_profile_service.get_customer_profile_by_user_id(
            curren_customer_user.id,
        )
    except CustomerProfileNotFoundError:
        raise CustomerProfileNotFoundHTTPException


CustomerProfileRequiredDI = Depends(get_customer_profile)
CustomerProfileDI = Annotated[CustomerProfileReadDTO, Depends(get_customer_profile)]
