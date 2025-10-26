import uvicorn
from fastapi import FastAPI
from starlette import status

from src.auth.controllers import auth_router
from src.core import config
from src.entities.service_category.controllers import service_categories_router
from src.entities.user.controllers import user_router


def include_routers(app: FastAPI):
    routers = (
        auth_router,
        user_router,
        service_categories_router,
    )
    for router in routers:
        app.include_router(router)


def get_app() -> FastAPI:
    app = FastAPI(
        title=config.api.title,
        debug=config.api.debug,
    )
    include_routers(app)
    return app


app = get_app()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "src.__main__:app",
        port=config.api.port,
        host=config.api.host,
    )
