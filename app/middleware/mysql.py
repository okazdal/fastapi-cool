from settings import GET


def get_db_url(db_info):
    engine = db_info.get("ENGINE")
    host = db_info.get("HOST")
    port = db_info.get("PORT")
    user = db_info.get("USER")
    password = db_info.get("PASSWORD")
    name = db_info.get("NAME")

    return f"{engine}://{user}:{password}@{host}:{port}/{name}?charset=utf8"


DATABASE_URI = get_db_url(GET.DATABASE)

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URI,
    },
    "apps": {
        "models": {"models": ["app.models.users"], "default_connection": "default"}
    }
}
