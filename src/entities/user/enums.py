from enum import StrEnum


class UserRole(StrEnum):
    USER = "customer"
    NOTARY = "notary"
    ADMIN = "admin"
