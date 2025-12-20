from src.core.exceptions.domain import BaseDomainError


class UserNotFoundError(BaseDomainError):
    def __str__(self) -> str:
        return "User not found"


class UsernameAlredyExistsError(BaseDomainError):
    def __init__(self, username: str):
        self.username = username

    def __str__(self) -> str:
        return f"User with username {self.username} already exists"
