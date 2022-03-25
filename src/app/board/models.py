from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.user.models import User


class Category(models.Model):
    """Category for project
    """
    name = fields.CharField(max_length=150)
    parent: fields.ForeignKeyNullableRelation['Category'] = fields.ForeignKeyField(
        'models.Category', related_name='children', null=True
    )
    children: fields.ReverseRelation['Category']
    projects: fields.ReverseRelation['Project']

    # class PydanticMeta:
    #     allow_cycles = True
    #     max_recursion = 4


class Toolkit(models.Model):
    """Category for project
        """
    name = fields.CharField(max_length=150)
    parent = fields.ForeignKeyField('models.Toolkit', related_name='children', null=True)


class Project(models.Model):
    """Category for project
        """
    name = fields.CharField(max_length=150)
    description = fields.TextField()
    create_date = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField('models.User', related_name='projects')
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        'models.Category', related_name='projects'
    )
    toolkit = fields.ForeignKeyField('models.Toolkit', related_name='projects')
    team = fields.ManyToManyField('models.User', related_name='team_projects')


class Task(models.Model):
    """ Model task by project
    """
    description = fields.TextField()
    create_date = fields.DatetimeField(auto_now_add=True)
    start_date = fields.DatetimeField(null=True)
    end_date = fields.DatetimeField(null=True)
    project = fields.ForeignKeyField('models.Project', related_name='tasks')
    worker = fields.ForeignKeyField('models.User', related_name='tasks', null=True)


class CommentTask(models.Model):
    """ Model task by task
    """
    user = fields.ForeignKeyField('models.User', related_name='task_comments')
    task = fields.ForeignKeyField('models.Task', related_name='comments')
    message = fields.CharField(max_length=1000)
    create_date = fields.DatetimeField(auto_now_add=True)


Tortoise.init_models(["src.app.board.models"], "models")
GetProject = pydantic_model_creator(Project, name='get_project',
                                    exclude=('user', 'tasks'))
