from typing import List

from fastapi import APIRouter, Depends
from .. import schemas, models, service
from ...auth.permissions import get_user

project_router = APIRouter()


@project_router.post('/', response_model=schemas.OutProject)
async def create_project(schema: schemas.CreateProject, user: models.User = Depends(get_user)):
    return await service.project_s.create(schema, user_id=user.id)


@project_router.get('/', response_model=List[schemas.OutProject])
async def get_list_projects():
    return await service.project_s.all()


@project_router.delete('/{pk}', status_code=204)
async def delete_project(pk: int, user: models.User = Depends(get_user)):
    return await service.project_s.delete(id=pk)
