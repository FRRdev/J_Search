from typing import List

from fastapi import APIRouter
from .. import schemas, models, service

project_router = APIRouter()


@project_router.post('/', response_model=schemas.GetProject)
async def create_project(schema: schemas.CreateProject):
    return await service.project_s.create(schema)


@project_router.get('/', response_model=List[schemas.GetProject])
async def get_list_projects():
    return await schemas.GetProject.from_queryset(models.Project.all())
