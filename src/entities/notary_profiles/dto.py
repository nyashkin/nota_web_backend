from datetime import datetime

from pydantic import Field, PositiveInt

from src.core.dto import BaseDTO


class NotaryProfileCreateDTO(BaseDTO):
    phone_number: str = Field(max_length=32)
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    license_number: str = Field(max_length=128)
    inn: str = Field(max_length=128)
    description: str = Field(max_length=256)


class NotaryProfileReadDTO(NotaryProfileCreateDTO):
    id: PositiveInt
    user_id: PositiveInt
    updated_at: datetime
    created_at: datetime


class NotaryProfileUpdateDTO(BaseDTO):
    phone_number: str | None = Field(None, max_length=32)
    first_name: str | None = Field(None, max_length=32)
    last_name: str | None = Field(None, max_length=32)
    license_number: str = Field(max_length=128)
    inn: str = Field(max_length=128)
    description: str = Field(max_length=256)
