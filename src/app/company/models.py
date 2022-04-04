from sqlalchemy.testing import exclude
from tortoise import fields, models, Tortoise

from src.app.user.models import User


class Classification(models.Model):
    """Category for company
    """
    name = fields.CharField(max_length=150)
    parent: fields.ForeignKeyNullableRelation['Classification'] = fields.ForeignKeyField(
        'models.Classification', related_name='children', null=True
    )
    children: fields.ReverseRelation['Classification']
    companies: fields.ReverseRelation['Company']

    class PydanticMeta:
        backward_relations = True
        exclude = ["companies", "parent"]
        allow_cycles = True
        max_recursion = 4


class Address(models.Model):
    """Category for company
    """
    country = fields.CharField(max_length=150)
    city = fields.CharField(max_length=150)
    street = fields.CharField(max_length=150, null=True)
    house = fields.CharField(max_length=150, null=True)
    company: fields.ForeignKeyRelation['Company'] = fields.ForeignKeyField(
        'models.Company', related_name='addresses'
    )


class Company(models.Model):
    """ Model of Company
    """
    name = fields.CharField(max_length=150)
    create_date = fields.DatetimeField(auto_now_add=True)
    classification: fields.ForeignKeyRelation[Classification] = fields.ForeignKeyField(
        'models.Classification', related_name='companies'
    )
    owner: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User', related_name='companies'
    )

    addresses: fields.ReverseRelation['Address']
    workers: fields.ReverseRelation[User]
    vacancies: fields.ReverseRelation['Vacancy']

    class PydanticMeta:
        backward_relations = False
        exclude = ["classification", ]


class Skill(models.Model):
    text = fields.CharField(max_length=150)

    # vacancies: fields.ManyToManyRelation['Vacancy']

    class PydanticMeta:
        backward_relations = False


class Vacancy(models.Model):
    name = fields.CharField(max_length=150)
    description = fields.TextField()
    salary = fields.IntField()
    create_date = fields.DatetimeField(auto_now_add=True)
    company: fields.ForeignKeyRelation[Company] = fields.ForeignKeyField(
        'models.Company', related_name='vacancies'
    )
    vacancy_skills: fields.ManyToManyRelation[Skill] = fields.ManyToManyField(
        'models.Skill', related_name='vacancies'
    )

    class PydanticMeta:
        backward_relations = False


class Offer(models.Model):
    vacancy: fields.ForeignKeyRelation['Vacancy'] = fields.ForeignKeyField(
        'models.Vacancy', related_name='offers_by_vacancy'
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User', related_name='offers_by_user'
    )


Tortoise.init_models(["src.app.company.models"], "models")
