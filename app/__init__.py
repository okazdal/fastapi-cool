from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise
from app.middleware.mysql import TORTOISE_ORM
from app.api.routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    app.debug = True

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(app)

    return app
