from typing import List

from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_user
from src.app.user import models, schemas, service

user_router = APIRouter()


@user_router.get('/me', response_model=schemas.UserPublic)
def user_me(current_user: models.User = Depends(get_user)):
    """ Get user"""
    if current_user:
        return current_user


@user_router.get('/', response_model=List[schemas.UserPublic])
async def get_all_users():
    """ Get user"""
    return await service.user_s.all()


@user_router.post('/', response_model=schemas.UserInDB)
async def create_users(schema: schemas.UserCreate):
    """ Create user"""
    return await service.user_s.create_user(schema)


@user_router.get('/{pk}', response_model=schemas.UserInDB)
async def get_single_user(pk: int):
    """ get single user"""
    return await service.user_s.get(id=pk)


@user_router.put('/{pk}', response_model=schemas.UserPublic)
async def update_user(pk: int, schema: schemas.UserUpdate):
    """ Update user"""
    return await service.user_s.update(schema, id=pk)


@user_router.delete('/{pk}', status_code=204)
async def delete_user(pk: int):
    """ Delete user"""
    return await service.user_s.delete(id=pk)
