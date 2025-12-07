from datetime import datetime

from pydantic import Field, PositiveInt

from src.core.dto import BaseDTO


class CustomerProfileCreateDTO(BaseDTO):
    phone_number: str = Field(max_length=32)
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)


class CustomerProfileReadDTO(CustomerProfileCreateDTO):
    id: PositiveInt
    user_id: PositiveInt
    updated_at: datetime
    created_at: datetime


class CustomerProfileUpdateDTO(BaseDTO):
    phone_number: str | None = Field(None, max_length=32)
    first_name: str | None = Field(None, max_length=32)
    last_name: str | None = Field(None, max_length=32)
