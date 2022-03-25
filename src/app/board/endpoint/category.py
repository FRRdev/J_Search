from typing import List

from fastapi import APIRouter
from .. import schemas, models, service

category_router = APIRouter()


@category_router.post('/', response_model=schemas.GetCategory)
async def create_category(schema: schemas.CreateCategory):
    return await service.category_s.create(schema)


@category_router.get('/', response_model=List[schemas.GetCategory])
async def create_category():
    return await service.category_s.all()
