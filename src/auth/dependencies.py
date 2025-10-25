from fastapi import Depends
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer

from src.auth.enums import AuthUrls
from src.auth.services import AuthService, CryptoService
from src.entities.user.dependencies import UserServiceDI
from src.entities.user.schemas import UserReadSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=AuthUrls.LOGIN_URL, refreshUrl=AuthUrls.REFRESH_URL
)

AuthServiceDI = Annotated[AuthService, Depends()]


async def get_current_user(
    user_service: UserServiceDI, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserReadSchema:
    user_payload = CryptoService.get_payload(token)

    user = await user_service.get_user_by_id(int(user_payload.sub))
    return user


CurrentUserDI = Annotated[UserReadSchema, Depends(get_current_user)]
