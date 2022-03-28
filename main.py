from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
#from src.db.session import Sessionlocal

from src.app import routers

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title="Useful",
    description="Author - DJWOMS",
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

register_tortoise(
    app,
    db_url=settings.DATABASE_URI_LOCAL,
    modules={"models": [
        "src.app.user.models",
        "src.app.auth.models",
        "aerich.models",
        "src.app.board.models",
    ]},
    #generate_schemas=True,
    add_exception_handlers=True,
)
