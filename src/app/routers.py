from fastapi import APIRouter
from src.app.auth.api import auth_router
from src.app.user.api import user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=["login"])
api_router.include_router(user_router, prefix='/user', tags=["user"])
