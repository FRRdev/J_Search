from typing import List

from fastapi import APIRouter, Depends
from .. import schemas, models, service
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
