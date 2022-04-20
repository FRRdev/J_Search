from datetime import datetime
from typing import List

from pydantic.main import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from . import models
from src.app.user.schemas import UserPublic
from ..company.schemas import CompanyOut

CreateCategory = pydantic_model_creator(models.Category, name='create_category', exclude_readonly=True)
GetCategory = pydantic_model_creator(models.Category, name='get_category')


class OutCategory(BaseModel):
    id: int
    name: str


CreateToolkit = pydantic_model_creator(models.Toolkit, name='create_toolkit', exclude_readonly=True)
GetToolkit = pydantic_model_creator(models.Toolkit, name='get_toolkit')


class OutToolkit(BaseModel):
    id: int
    name: str


CreateProject = pydantic_model_creator(models.Project, name='create_project', exclude=('user_id',),
                                       exclude_readonly=True)
GetProject = pydantic_model_creator(models.Project, name='get_project')


class OutProject(PydanticModel):
    id: int
    name: str
    description: str
    create_date: datetime
    user: UserPublic
    category: OutCategory
    toolkit: OutToolkit
    company: CompanyOut = None


class Category(PydanticModel):
    id: int
    name: str

    class Config:
        orm_mode = True


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
                "start_date": "2020-10-18 15:26:17",
                "end_date": "2020-10-18 15:26:17",
                "project_id": 0,
                "worker_id": 0,
            }
        }


GetTask = pydantic_model_creator(models.Task, name='get_task')


class CreateCommentTask(PydanticModel):
    user_id: int
    task_id: int
    message: str


GetCommentTask = pydantic_model_creator(models.CommentTask, name='get_comment_task')


class CreateTeam(BaseModel):
    project: int
    team: List[int]
