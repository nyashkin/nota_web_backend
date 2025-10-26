from src.core.exceptions.domain import BaseDomainException


class UknownServiceException(BaseDomainException):
    def __str__(self) -> str:
        return "Uknown service exception"
