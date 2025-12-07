from src.core.exceptions.domain import BaseDomainException


class ServiceCategoryNotFoundException(BaseDomainException):
    def __str__(self) -> str:
        return "Service category not found"


class ServiceCategoryCreateException(BaseDomainException):
    def __str__(self) -> str:
        return "Service category name is not unique or parent is not exists"


class ParentServiceCategoryNotFoundException(BaseDomainException):
    def __str__(self) -> str:
        return "Parent service category is not exists"


class ServiceCategoryIdAndParentIdCannotBeEqualException(BaseDomainException):
    def __str__(self) -> str:
        return "Service category id and parent id cannot be equal exception"
