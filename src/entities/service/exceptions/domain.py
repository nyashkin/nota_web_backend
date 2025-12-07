from src.core.exceptions.domain import BaseDomainException


class ServiceNotFoundException(BaseDomainException):
    def __init__(self, service_id: int) -> None:
        self.service_id = service_id

    def __str__(self) -> str:
        return f"Service with id {self.service_id} not found"


class ServiceCategoryForServiceNotFoundException(BaseDomainException):
    def __init__(self, service_category_id: int) -> None:
        self.service_category_id = service_category_id

    def __str__(self) -> str:
        return f"Service category with id {self.service_category_id} not found"


class NotUniqueServiceTitleException(BaseDomainException):
    def __init__(self, title: str) -> None:
        self.title = title

    def __str__(self) -> str:
        return f"Service with title {self.title} already exists"
