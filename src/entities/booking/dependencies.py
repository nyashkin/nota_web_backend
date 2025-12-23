from fastapi import Depends
from typing_extensions import Annotated

from src.entities.booking.service import BookingService

BookingServiceDI = Annotated[BookingService, Depends()]
