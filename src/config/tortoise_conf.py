from src.config.settings import DATABASE_URI_LOCAL, APPS_MODELS,DATABASE_URI_TEST,TESTING


database_uri = DATABASE_URI_TEST if TESTING else DATABASE_URI_LOCAL


TORTOISE_ORM = {
    "connections": {"default": database_uri},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        },
    },
}
