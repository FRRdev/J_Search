from typing import Optional

from fastapi import HTTPException

from . import schemas, models
from ..base.service_sql_base import BaseService
from ..company.models import Company


class CategoryService(BaseService):
    model = models.Category
    create_schema = schemas.CreateCategory
    get_schema = schemas.GetCategory


class ToolkitService(BaseService):
    model = models.Toolkit
    create_schema = schemas.CreateToolkit
    get_schema = schemas.GetToolkit


class ProjectService(BaseService):
    model = models.Project
    create_schema = schemas.CreateProject
    get_schema = schemas.GetProject


class TaskService(BaseService):
    model = models.Task
    create_schema = schemas.CreateTask
    get_schema = schemas.GetTask

    async def task_create(self, schema: schemas.CreateTask) -> Optional[schemas.GetTask]:
        abble_to_create = await Company.filter(
            projects_by_company=schema.project_id, vacancies__offers_by_vacancy__user_id=schema.worker_id
        ).exists()
        if not abble_to_create:
            raise HTTPException(status_code=404, detail='Project and worker not from one company')
        else:
            return await super().create(schema)


class CommentTaskService(BaseService):
    model = models.CommentTask
    create_schema = schemas.CreateCommentTask
    get_schema = schemas.GetCommentTask


category_s = CategoryService()
toolkit_s = ToolkitService()
project_s = ProjectService()
task_s = TaskService()
comment_task_s = CommentTaskService()
