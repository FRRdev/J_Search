from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
# from src.db.session import Sessionlocal


from src.app import routers

from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, run_async

app = FastAPI(
    title="Useful",
    description="Author - FRRDev",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(routers.api_router, prefix=settings.API_V1_STR)

if settings.TESTING:
    register_tortoise(
        app,
        config={
            "connections": {"default": settings.DATABASE_URI_TEST},
            "apps": {"models": {"models": settings.APPS_MODELS}},
            "use_tz": True,
            "timezone": "Asia/Shanghai",
            "generate_schemas": True,
        },
    )
else:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI_LOCAL,
        modules={"models": settings.APPS_MODELS},
        # generate_schemas=True,
        add_exception_handlers=True,
    )
