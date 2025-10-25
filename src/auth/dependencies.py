from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.auth.enums import AuthUrls, TokenType
from src.auth.exceptions.http import InvalidJwtTokenTypeError
from src.auth.services import AuthService, CryptoService
from src.core.exceptions.http import BaseHTTPException
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.enums import UserRole
from src.entities.user.exceptions.domain import (
    UserNotFoundException,
    UserUknownException,
)
from src.entities.user.exceptions.http import UserNotFoundError, UserUknownError
from src.entities.user.schemas import UserReadSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=AuthUrls.LOGIN_URL, refreshUrl=AuthUrls.REFRESH_URL
)

AuthServiceDI = Annotated[AuthService, Depends()]


async def get_current_user(
    user_service: UserServiceDI, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserReadSchema:
    payload = CryptoService.get_payload(token)
    if payload.type == TokenType.REFRESH:
        raise InvalidJwtTokenTypeError
    try:
        user = await user_service.get_user_by_id(int(payload.sub))
    except UserNotFoundException as e:
        raise UserNotFoundError(e)
    except UserUknownException:
        raise UserUknownError
    return user


AuthRequiredDI = Depends(get_current_user)

CurrentUserDI = Annotated[UserReadSchema, AuthRequiredDI]


async def check_admin_access(current_user: CurrentUserDI) -> UserReadSchema:
    if current_user.role != UserRole.ADMIN:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return current_user


AdminRequiredDI = Depends(check_admin_access)


async def check_user_access(current_user: CurrentUserDI) -> UserReadSchema:
    if current_user.role != UserRole.USER:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return current_user


UserRequiredDI = Depends(check_user_access)
