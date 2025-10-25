from typing import Annotated

from fastapi import Depends

from src.entities.user.services import UserService

UserServiceDI = Annotated[UserService, Depends(UserService)]
