from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings

from src.app import routers

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title="J_Search",
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
app.mount("/media", StaticFiles(directory="media"), name="media")

register_tortoise(
    app,
    db_url=settings.DATABASE_URI_LOCAL,
    modules={"models": settings.APPS_MODELS},
    # generate_schemas=True,
    add_exception_handlers=True,
)
