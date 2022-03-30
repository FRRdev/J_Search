from typing import List

from fastapi import APIRouter, Depends
from .. import schemas, models, service
from ...auth.permissions import get_superuser

company_router = APIRouter()


@company_router.post('/', response_model=schemas.GetCompany)
async def create_company(
        schema: schemas.CreateCompany,
        user: models.User = Depends(get_superuser)
):
    """ Create company router
    """
    return await service.company_s.create(schema)


@company_router.post('/classification', response_model=schemas.GetClassification)
async def create_classification(
        schema: schemas.CreateClassification,
        user: models.User = Depends(get_superuser)
):
    """ Create classification router
    """
    return await service.classification_s.create(schema)
