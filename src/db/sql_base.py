from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from src.config import settings


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI_LOCAL,
        modules={"models": settings.APPS_MODELS},
        generate_schemas=False,
        add_exception_handlers=True,
    )
    Tortoise.init_models(["src.app.company.models", "src.app.board.models"], "models")
