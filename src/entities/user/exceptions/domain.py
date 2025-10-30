from src.core.exceptions.domain import BaseDomainException


class UserNotFoundException(BaseDomainException):
    def __str__(self) -> str:
        return "User not found"


class UsernameAlredyExistsException(BaseDomainException):
    def __init__(self, username: str):
        self.username = username

    def __str__(self) -> str:
        return f"User with username {self.username} already exists"
