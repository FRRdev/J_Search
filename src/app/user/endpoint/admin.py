from typing import List

from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser
from src.app.user import models, schemas, service

admin_router = APIRouter()


@admin_router.get('/', response_model=List[schemas.UserBaseInDB])
async def get_all_users(user: models.User = Depends(get_superuser)):
    """ Get user"""
    return await service.user_s.all()


@admin_router.post('/', response_model=schemas.UserInDB)
async def create_users(schema: schemas.UserCreate, user: models.User = Depends(get_superuser)):
    """ Create user"""
    return await service.user_s.create_user(schema)


@admin_router.get('/{pk}', response_model=schemas.UserInDB)
async def get_single_user(pk: int, user: models.User = Depends(get_superuser)):
    """ get single user"""
    return await service.user_s.get(id=pk)


@admin_router.put('/{pk}', response_model=schemas.UserPublic)
async def update_user(pk: int, schema: schemas.UserUpdate, user: models.User = Depends(get_superuser)):
    """ Update user"""
    return await service.user_s.update_user(schema, id=pk)


@admin_router.delete('/{pk}', status_code=204)
async def delete_user(pk: int, user: models.User = Depends(get_superuser)):
    """ Delete user"""
    return await service.user_s.delete(id=pk)
