from . import schemas, models
from ..base.service_base import BaseService


class CompanyService(BaseService):
    model = models.Company
    create_schema = schemas.CreateCompany
    get_schema = schemas.GetCompany


class ClassificationService(BaseService):
    model = models.Classification
    create_schema = schemas.CreateClassification
    get_schema = schemas.GetClassification


company_s = CompanyService()
classification_s = ClassificationService()
