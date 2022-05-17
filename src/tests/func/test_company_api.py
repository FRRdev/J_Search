import pytest
from httpx import AsyncClient
from main import app

from src.app.company.schemas import GetClassification
from src.app.company import models


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_create_classification(company_user_token):
    company_user, company_user_access_token = company_user_token
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        example_value = {"name": "IT", }
        classification_it_response = await ac.post(
            "/api/v1/company/classification", headers={'Authorization': f'Bearer {company_user_access_token}'},
            json=example_value
        )
        classification_it_obj = await models.Classification.get(name='IT')
        classification_it_data = await GetClassification.from_tortoise_orm(classification_it_obj)
        assert classification_it_response.json() == classification_it_data
        assert classification_it_response.status_code == 200
        example_value = {"name": "Finnance", }
        classification_fin_response = await ac.post(
            "/api/v1/company/classification", json=example_value,
            headers={'Authorization': f'Bearer {company_user_access_token}'}
        )
        classification_fin_obj = await models.Classification.get(name='Finnance')
        classification_fin_data = await GetClassification.from_tortoise_orm(classification_fin_obj)
        assert classification_fin_response.json() == classification_fin_data
        assert classification_it_response.status_code == 200


@pytest.mark.asyncio
async def test_list_classification(company_user_token):
    company_user, company_user_access_token = company_user_token
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        classification_response = await ac.get("/api/v1/company/classification",
                                               headers={'Authorization': f'Bearer {company_user_access_token}'})
        assert classification_response.status_code == 200
        assert len(classification_response.json()) == 2


@pytest.mark.asyncio
async def test_create_company(company_user_token, no_company_user_token):
    company_user, company_user_access_token = company_user_token
    no_company_user, no_company_user_access_token = no_company_user_token
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        data = {
            "name": "someCompany",
            "classification_id": 1
        }
        company_response = await ac.post(
            "/api/v1/company/", json=data, headers={'Authorization': f'Bearer {company_user_access_token}'}
        )
        company_response_data = company_response.json()
        assert company_response.status_code == 200
        assert company_response_data['id'] == 1
        assert company_response_data['name'] == 'someCompany'
        assert company_response_data['owner'] == {'first_name': company_user.first_name, 'id': company_user.id}
        company_response_incorrect = await ac.post(
            "/api/v1/company/", json=data, headers={'Authorization': f'Bearer {no_company_user_access_token}'}
        )
        error_meessage = {'detail': 'User does not have privileges of company'}
        assert company_response_incorrect.json() == error_meessage


@pytest.mark.asyncio
async def test_create_address(company_user_token, no_company_user_token):
    company_user, company_user_access_token = company_user_token
    no_company_user, no_company_user_access_token = no_company_user_token
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        data = {
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "house": "12",
            "company_id": 1
        }
        address_response = await ac.post(
            "/api/v1/company/address", json=data, headers={'Authorization': f'Bearer {company_user_access_token}'}
        )
        correct_address_response = {
            "id": 1,
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "house": "12",
            "company": {
                "id": 1,
                "name": "someCompany"
            }
        }
        assert address_response.status_code == 200
        assert address_response.json() == correct_address_response
        company_response_incorrect = await ac.post(
            "/api/v1/company/", json=data, headers={'Authorization': f'Bearer {no_company_user_access_token}'}
        )
        error_meessage = {'detail': 'User does not have privileges of company'}
        assert company_response_incorrect.json() == error_meessage


@pytest.mark.asyncio
async def test_list_address(company_user_token):
    company_user, company_user_access_token = company_user_token
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        address_response = await ac.get(
            "/api/v1/company/address", headers={'Authorization': f'Bearer {company_user_access_token}'}
        )
        correct_address_response = {
            "id": 1,
            "country": "Russia",
            "city": "Moscow",
            "street": "Lenina",
            "house": "12",
            "company": {
                "id": 1,
                "name": "someCompany"
            }
        }
        assert address_response.status_code == 200
        assert len(address_response.json()) == 1
        assert correct_address_response in address_response.json()


@pytest.mark.asyncio
async def test_put_address(company_user_token):
    company_user, company_user_access_token = company_user_token
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        data = {
            "country": "USA",
            "city": "New York City",
            "street": "string",
            "house": "12",
            "company_id": 1
        }
        address_response = await ac.put(
            "/api/v1/company/address/1", json=data, headers={'Authorization': f'Bearer {company_user_access_token}'}
        )
        correct_address_response = {
            "id": 1,
            "country": "USA",
            "city": "New York City",
            "street": "string",
            "house": "12",
            "company": {
                "id": 1,
                "name": "someCompany"
            }
        }
        assert address_response.status_code == 200
        assert correct_address_response == address_response.json()
