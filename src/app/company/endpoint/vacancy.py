from typing import List

from fastapi import APIRouter, Depends, Form, Query
from .. import schemas, models, service
from ..schemas import MSG
from ...auth.permissions import get_superuser, get_user

vacancy_router = APIRouter()


@vacancy_router.post('/skill', response_model=schemas.GetSkill)
async def create_skill(
        schema: schemas.CreateSkill,
        user: models.User = Depends(get_user)
):
    """ Create skill router
    """
    return await service.skill_s.create(schema)


@vacancy_router.get('/skill', response_model=List[schemas.GetSkill])
async def get_list_classification():
    return await service.skill_s.all()


@vacancy_router.post('/', response_model=schemas.VacancyOut)
async def create_vacancy(
        vacancy: schemas.CreateVacancy,
        skills: List[int],
        user: models.User = Depends(get_user)
):
    """ Create vacancy router
    """
    return await service.vacancy_s.vacancy_create(vacancy, skills)


@vacancy_router.get('/', response_model=List[schemas.VacancyOut])
async def get_list_vacancies():
    """ Get list vacancies router
    """
    return await service.vacancy_s.list_vacancies()


@vacancy_router.get('/{pk}', response_model=schemas.GetVacancy)
async def get_single_vacancy(pk: int):
    """ Get single vacancy router
    """
    return await service.vacancy_s.get(id=pk)


@vacancy_router.post('/{pk}', status_code=204)
async def create_delete_offer_to_vacancy(pk: int, user: models.User = Depends(get_user)):
    """ Get single vacancy router
    """
    return await service.offer_s.create_or_delete_offer(user_id=user.id, vacancy_id=pk)


@vacancy_router.delete('/{pk}', status_code=204)
async def delete_vacancy(pk: int, user: models.User = Depends(get_superuser)):
    return await service.vacancy_s.delete(id=pk)


@vacancy_router.get('/search/', response_model=List[schemas.VacancyOut])
async def search_vacancies(info: str = Query(...)):
    """ Search vacancy by some field
    """
    return await service.vacancy_s.list_vacancies_by_info(info)
# @vacancy_router.get('/test', status_code=201)
# async def get_test():
#     """ Get list vacancies router
#     """
#     data = await Vacancy.all().prefetch_related('vacancy_skills')
#     data = data[0]
#     data = data.vacancy_skills
#     for d in data:
#         print(d.id)
#     data = await service.vacancy_s.all()
#     data = data[0]
#     print(data)
#     skills = data.vacancy_skills
#     for s in skills:
#         print(s.id)
