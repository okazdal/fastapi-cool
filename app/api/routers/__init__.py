from .websocket import app as websocket_router
from .users import app as users_router


def init_routers(app):
    app.include_router(websocket_router)
    app.include_router(users_router, prefix="/users")
