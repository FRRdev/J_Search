from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from . import models

from src.app.user.schemas import UserPublic
# GetCategory = pydantic_model_creator(models.Category, name='get_category')

class GetCategory(PydanticModel):
    name: str
    parent_id: int = None


class CreateCategory(PydanticModel):
    name: str
    parent_id: int = None


GetToolkit = pydantic_model_creator(models.Toolkit, name='get_toolkit')


class CreateToolkit(PydanticModel):
    name: str
    parent_id: int = None


class CreateProject(PydanticModel):
    name: str
    description: str
    category_id: int
    user_id: int
    toolkit_id: int


# GetProject = pydantic_model_creator(models.Project, name='get_project')

class GetProject(PydanticModel):
    name: str
    description: str
    create_date: datetime
    category: GetCategory

    class Config:
        orm_mode = True


GetTask = pydantic_model_creator(models.Task, name='get_task')


class CreateTask(PydanticModel):
    description: str
    start_date: datetime
    end_date: datetime
    project_id: int
    worker_id: int = None

    class Config:
        schema_extra = {
            "example": {
                "description": "string",
                "start_date": "2022-10-18 15:26:17",
                "end_date": "2022-10-19 15:26:17",
                "project_id": 0,
                "worker_id": 0,
            }
        }


GetCommentTask = pydantic_model_creator(models.CommentTask, name='get_comment_task')


class CreateCommentTask(PydanticModel):
    user_id: int
    task_id: int
    message: str
