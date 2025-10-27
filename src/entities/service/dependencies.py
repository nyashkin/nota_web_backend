from typing import Annotated

from fastapi import Depends

from src.entities.service.services import ServiceService

ServiceServiceDI = Annotated[ServiceService, Depends()]
