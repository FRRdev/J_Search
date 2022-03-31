from datetime import datetime
from typing import List

from pydantic.main import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from . import models

CreateClassification = pydantic_model_creator(models.Classification, exclude_readonly=True)
GetClassification = pydantic_model_creator(models.Classification, name='get_class')

CreateCompany = pydantic_model_creator(models.Company, exclude_readonly=True)
GetCompany = pydantic_model_creator(models.Company)


class CompanyOut(BaseModel):
    id: int
    name: str


CreateAddress = pydantic_model_creator(models.Address, exclude_readonly=True)
GetAddress = pydantic_model_creator(models.Address)


class AddressOut(PydanticModel):
    id: int
    country: str
    city: str
    street: str
    house: str
    company: CompanyOut
