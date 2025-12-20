from src.core.exceptions.domain import BaseDomainError


class ServiceCategoryNotFoundError(BaseDomainError):
    def __str__(self) -> str:
        return "Service category not found"


class ServiceCategoryCreateError(BaseDomainError):
    def __str__(self) -> str:
        return "Service category name is not unique or parent is not exists"


class ParentServiceCategoryNotFoundError(BaseDomainError):
    def __str__(self) -> str:
        return "Parent service category is not exists"


class ServiceCategoryIdAndParentIdCannotBeEqualError(BaseDomainError):
    def __str__(self) -> str:
        return "Service category id and parent id cannot be equal exception"
