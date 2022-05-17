from fastapi import APIRouter, Depends
from .. import schemas, models, service
from ...auth.permissions import get_user

task_router = APIRouter()


@task_router.post('/', response_model=schemas.GetTask)
async def create_task(schema: schemas.CreateTask, user: models.User = Depends(get_user)):
    return await service.task_s.task_create(schema)


@task_router.post('/comment', response_model=schemas.GetCommentTask)
async def create_comment_task(schema: schemas.CreateCommentTask):
    return await service.comment_task_s.create(schema)

