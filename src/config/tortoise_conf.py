from src.config.settings import DATABASE_URI, DATABASE_URI_LOCAL, APPS_MODELS

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URI_LOCAL},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        },
    },
}
