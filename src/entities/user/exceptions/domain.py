from src.core.exceptions.domain import BaseDomainException
from src.entities.user.schemas import UserBaseSchema


class BaseUserException(BaseDomainException):
    def __init__(self, user: UserBaseSchema):
        self.user = user


class UserNotFoundException(BaseUserException):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self) -> str:
        return f"User with id {self.user_id} not found"


class UserAlredyExistsException(BaseUserException):
    def __init__(self, username: str):
        self.username = username

    def __str__(self) -> str:
        return f"User with username {self.username} already exists"


class UserUknownException(BaseUserException):
    def __init__(self, exc: BaseException):
        self.exc = exc

    def __str__(self) -> str:
        return f"User uknown exception: {self.exc}"
