from typing import Optional

from tortoise.expressions import Q

from . import schemas, models
from ..base.service_base import BaseService, CreateSchemaType

from .schemas import VacancyOut


class CompanyService(BaseService):
    model = models.Company
    create_schema = schemas.CreateCompany
    get_schema = schemas.GetCompany


class ClassificationService(BaseService):
    model = models.Classification
    create_schema = schemas.CreateClassification
    get_schema = schemas.GetClassification


class AddressService(BaseService):
    model = models.Address
    create_schema = schemas.CreateAddress
    get_schema = schemas.GetAddress


class VacancyService(BaseService):
    model = models.Vacancy
    create_schema = schemas.CreateVacancy
    get_schema = schemas.GetVacancy

    async def vacancy_create(self, schema, skills, **kwargs) -> Optional[schemas.CreateVacancy]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        _skills = await models.Skill.filter(id__in=skills)
        await obj.vacancy_skills.add(*_skills)
        return await self.model.get(id=obj.id).prefetch_related('vacancy_skills').select_related('company')

    async def list_vacancies(self) -> Optional[schemas.GetVacancy]:
        data = await self.model.all().prefetch_related('vacancy_skills').select_related('company')
        return data

    async def list_vacancies_by_info(self, info: str) -> Optional[schemas.GetVacancy]:
        data = await self.model.filter(Q(name__icontains=info) | Q(description__icontains=info)).prefetch_related(
            'vacancy_skills').select_related('company')
        return data


class SkillService(BaseService):
    model = models.Skill
    create_schema = schemas.CreateSkill
    get_schema = schemas.GetSkill


class OfferService(BaseService):
    model = models.Offer
    create_schema = schemas.CreateOffer
    get_schema = schemas.GetOffer

    async def create_or_delete_offer(self, **kwargs) -> dict:
        obj = await self.model.filter(**kwargs).exists()
        if obj:
            await self.delete(**kwargs)
            return {"msg": "Offer deleted successfully"}
        await self.model.create(**kwargs)
        return {"msg": "Offer created successfully"}

    # async def accept_offer(self, **kwargs) -> dict:
    #     obj = await self.model.filter(**kwargs).select_related('user', 'vacancy').first()
    #     if obj:
    #         user_to_add = await obj.user
    #         current_company = await obj.vacancy.company
    #         user_to_add.company = current_company
    #         await user_to_add.save()
    #         await self.delete(**kwargs)
    #         return {"msg": "User is hired successfully"}
    #     return {"msg": "User does not exist"}

    async def delete_offer(self, **kwargs) -> dict:
        obj = await self.model.filter(**kwargs).select_related('user', 'vacancy').first()
        if obj:
            await self.delete(**kwargs)
            return {"msg": "user rejected successfully"}
        return {"msg": "User does not exist"}


company_s = CompanyService()
classification_s = ClassificationService()
address_s = AddressService()
vacancy_s = VacancyService()
skill_s = SkillService()
offer_s = OfferService()
