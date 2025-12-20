from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.auth.enums import AuthUrls, TokenType
from src.auth.exceptions.http import (
    AccessDeniedHTTPException,
    InvalidJwtTokenTypeHTTPException,
    NotAuthenticatedHTTPException,
)
from src.auth.services import AuthService, CryptoService
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.dto import UserReadDTO
from src.entities.user.enums import UserRoleEnum
from src.entities.user.exceptions.domain import (
    UserNotFoundError,
)
from src.entities.user.schemas import UserReadSchema

CryptoServiceDI = Annotated[CryptoService, Depends()]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=AuthUrls.LOGIN_URL,
    refreshUrl=AuthUrls.REFRESH_URL,
)

AuthServiceDI = Annotated[AuthService, Depends()]


async def get_current_user(
    user_service: UserServiceDI,
    crypto_service: CryptoServiceDI,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserReadDTO:
    payload = crypto_service.get_payload(token)
    if payload.type == TokenType.REFRESH:
        raise InvalidJwtTokenTypeHTTPException
    try:
        user = await user_service.get_user_by_id(int(payload.sub))
    except UserNotFoundError:
        raise NotAuthenticatedHTTPException
    return user


AuthRequiredDI = Depends(get_current_user)

CurrentUserDI = Annotated[UserReadSchema, AuthRequiredDI]


async def check_admin_access(current_user: CurrentUserDI) -> UserReadSchema:
    if current_user.role != UserRoleEnum.ADMIN:
        raise AccessDeniedHTTPException
    return current_user


AdminRoleRequiredDI = Depends(check_admin_access)
CurrentAdminUser = Annotated[UserReadSchema, AdminRoleRequiredDI]


async def check_customer_access(current_user: CurrentUserDI) -> UserReadSchema:
    if current_user.role != UserRoleEnum.CUSTOMER:
        raise AccessDeniedHTTPException
    return current_user


CustomerRoleRequiredDI = Depends(check_customer_access)
CurrentCustomerUser = Annotated[UserReadSchema, CustomerRoleRequiredDI]


async def check_notary_access(current_user: CurrentUserDI) -> UserReadSchema:
    if current_user.role != UserRoleEnum.NOTARY:
        raise AccessDeniedHTTPException
    return current_user


NotaryRoleRequiredDI = Depends(check_notary_access)
CurrentNotaryUser = Annotated[UserReadSchema, NotaryRoleRequiredDI]
