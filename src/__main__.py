from src.auth.controllers import auth_router
from src.entities.user.controllers import user_router
from fastapi import FastAPI
import uvicorn


def include_routers(app: FastAPI):
    routers = (
        auth_router,
        user_router,
    )
    for router in routers:
        app.include_router(router)


def get_app() -> FastAPI:
    app = FastAPI(debug=True)
    include_routers(app)
    return app


app = get_app()

if __name__ == "__main__":
    uvicorn.run("src.__main__:app")
