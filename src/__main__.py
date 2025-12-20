import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.auth.controllers import auth_router
from src.core import config
from src.entities.customer_profiles.controllers import customer_profiles_router
from src.entities.notary_profiles.controllers import notary_profiles_router
from src.entities.service.controllers import services_router
from src.entities.service_category.controllers import service_categories_router
from src.entities.user.controllers import user_router


def include_routers(app: FastAPI):
    routers = (
        auth_router,
        user_router,
        customer_profiles_router,
        notary_profiles_router,
        service_categories_router,
        services_router,
    )
    for router in routers:
        app.include_router(router)


def set_middlewares(app: FastAPI):
    origins = config.api.cors_origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def get_app() -> FastAPI:
    app = FastAPI(
        title=config.api.title,
        debug=config.api.debug,
    )

    @app.get(
        "/health",
        status_code=status.HTTP_200_OK,
        include_in_schema=False,
    )
    async def health() -> dict[str, str]:
        return {"message": "ok"}

    set_middlewares(app)
    include_routers(app)
    return app


app = get_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.__main__:app",
        port=config.api.port,
        host=config.api.host,
    )
