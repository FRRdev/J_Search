from src.config.settings import DATABASE_URI, DATABASE_URI_LOCAL

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URI_LOCAL},
    "apps": {
        "models": {
            "models": ["src.app.user.models", "src.app.auth.models", "aerich.models", "src.app.board.models"],
            "default_connection": "default",
        },
    },
}
