from src.core.exceptions.domain import BaseDomainError


class BookingsNotFoundError(BaseDomainError):
    def __str__(self) -> str:
        return "Bookings not found"
