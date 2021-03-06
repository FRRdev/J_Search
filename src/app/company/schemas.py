from datetime import datetime
from typing import List

from pydantic.main import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from . import models
from ..user.schemas import UserPublic

CreateClassification = pydantic_model_creator(models.Classification, name='create_classification',
                                              exclude_readonly=True)
GetClassification = pydantic_model_creator(models.Classification, name='get_class')

CreateCompany = pydantic_model_creator(models.Company, name='create_company', exclude=('owner_id',),
                                       exclude_readonly=True)
GetCompany = pydantic_model_creator(models.Company, name='get_company')


class CompanyOut(BaseModel):
    id: int
    name: str


class CompanyFullOut(PydanticModel):
    id: int
    name: str
    create_date: datetime
    classification: GetClassification
    owner: UserPublic


CreateAddress = pydantic_model_creator(models.Address, exclude_readonly=True)
GetAddress = pydantic_model_creator(models.Address)


class AddressOut(PydanticModel):
    id: int
    country: str
    city: str
    street: str
    house: str
    company: CompanyOut


CreateSkill = pydantic_model_creator(models.Skill, exclude_readonly=True)
GetSkill = pydantic_model_creator(models.Skill, exclude=('vacancies',), name='get_skill')

CreateVacancy = pydantic_model_creator(models.Vacancy, name='create_vacancy', exclude_readonly=True)
GetVacancy = pydantic_model_creator(models.Vacancy)


class VacancyOut(PydanticModel):
    id: int
    name: str
    description: str
    salary: str
    create_date: datetime
    company: CompanyOut
    vacancy_skills: List[GetSkill]


CreateOffer = pydantic_model_creator(models.Offer, exclude_readonly=True)
GetOffer = pydantic_model_creator(models.Offer)


class MSG(BaseModel):
    msg: str
