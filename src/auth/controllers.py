from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import AuthServiceDI
from src.auth.enums import AuthUrls
from src.auth.exceptions.domain import (
    InvalidJwtTokenException,
    JwtTokenExpiredException,
)
from src.auth.exceptions.http import InvalidJwtTokenError, JwtTokenExpiredError
from src.auth.schemas import AuthTokenRead
from src.core import config
from src.entities.user.exceptions.domain import (
    UserAlredyExistsException,
    UserByUsernameNotFoundException,
    UserNotFoundException,
    UserUknownException,
)
from src.entities.user.exceptions.http import (
    UserAlreadyExistsError,
    UserByUsernameNotFoundError,
    UserNotFoundError,
    UserUknownError,
)
from src.entities.user.schemas import UserCreateSchema, UserReadSchema

auth_router = APIRouter(prefix="/auth", tags=["🔑 Auth"])


@auth_router.post("/login", response_model=AuthTokenRead)
async def login(
    auth_service: AuthServiceDI,
    creds: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
) -> AuthTokenRead:
    try:
        token_read = await auth_service.login_user(
            username=creds.username, password=creds.password
        )
    except UserByUsernameNotFoundException:
        raise UserByUsernameNotFoundError
    except UserUknownException:
        raise UserUknownError

    response.set_cookie(
        key="refresh_token",
        value=token_read.refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=int(
            timedelta(days=config.auth.refresh_token_expire_days).total_seconds()
        ),
        path=AuthUrls.REFRESH_URL,
    )

    return AuthTokenRead(access_token=token_read.access_token)


@auth_router.post("/logout", response_model=AuthTokenRead)
async def logout(
    response: Response,
) -> dict[str, str]:
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="strict",
        path=AuthUrls.REFRESH_URL,
    )
    return {"message": "ok"}


@auth_router.post("/register", response_model=UserReadSchema)
async def register(
    auth_service: AuthServiceDI, create_user: UserCreateSchema
) -> UserReadSchema:
    try:
        user = await auth_service.register_user(create_user)
    except UserAlredyExistsException:
        raise UserAlreadyExistsError
    except UserUknownException:
        raise UserUknownError

    return user


@auth_router.post("/refresh", response_model=AuthTokenRead)
async def refresh(
    auth_service: AuthServiceDI, refresh_token: Annotated[str, Cookie()]
) -> AuthTokenRead:
    try:
        new_access_token = await auth_service.refresh_token(refresh_token)
    except JwtTokenExpiredException:
        raise JwtTokenExpiredError
    except InvalidJwtTokenException:
        raise InvalidJwtTokenError
    except UserNotFoundException as e:
        raise UserNotFoundError(e)
    except UserUknownException:
        raise UserUknownError
    return new_access_token
