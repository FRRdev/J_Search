from typing import List

from fastapi import APIRouter, Depends, Path
from .. import schemas, models, service
from ...auth.permissions import get_superuser, get_company, get_owner_company_by_address

company_router = APIRouter()


@company_router.post('/classification', response_model=schemas.GetClassification)
async def create_classification(
        schema: schemas.CreateClassification,
        user: models.User = Depends(get_superuser)
):
    """ Create classification router
    """
    return await service.classification_s.create(schema)


@company_router.get('/classification', response_model=List[schemas.GetClassification])
async def get_list_classification():
    return await service.classification_s.all()


@company_router.post('/address', response_model=schemas.AddressOut)
async def create_address(
        schema: schemas.CreateAddress,
        user: models.User = Depends(get_superuser)
):
    """ Create company router
    """
    return await service.address_s.create(schema)


@company_router.put('/address/{pk}', response_model=schemas.AddressOut)
async def update_address(
        pk: int, schema: schemas.CreateAddress,
        user: models.User = Depends(get_owner_company_by_address)
):
    return await service.address_s.update(schema, id=pk)


@company_router.get('/address', response_model=List[schemas.AddressOut])
async def get_list_address():
    """Get list of address
    """
    return await service.address_s.all()


@company_router.delete('/address/{pk}', status_code=204)
async def delete_address(pk: int, user: models.User = Depends(get_owner_company_by_address)):
    return await service.address_s.delete(id=pk)


@company_router.post('/', response_model=schemas.CompanyFullOut)
async def create_company(
        schema: schemas.CreateCompany,
        user: models.User = Depends(get_company)
):
    """ Create company router
    """
    return await service.company_s.create(schema, owner_id=user.id)


@company_router.get('/', response_model=List[schemas.CompanyFullOut])
async def get_list_company():
    """ Create company router
    """
    return await service.company_s.all()


@company_router.get('/{pk}', response_model=schemas.GetCompany)
async def get_single_company(pk: int = Path(...)):
    """ get singe company by pk
    """
    return await service.company_s.get(pk=pk)
