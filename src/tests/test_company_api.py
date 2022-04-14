import pytest
from httpx import AsyncClient
from main import app
from src.app.auth.security import get_password_hash
from src.app.user.models import User

company_user, no_company_user = User, User
company_user_access_token, no_company_user_access_token = None, None


@pytest.mark.asyncio
async def test_create_company_user():
    password = '123'
    password_hash = get_password_hash(password)
    global company_user
    company_user = await User.create(
        username='copmany_test', email='company2@mail.ru', password=password_hash, first_name='ComCorrect',
        is_active=True, is_superuser=True, is_company=True
    )
    password_hash = get_password_hash(password)
    global no_company_user
    no_company_user = await User.create(
        username='no_active_another', email='noact2@mail.ru', password=password_hash, first_name='ErrorUser2',
        is_active=True, is_superuser=False, is_company=False
    )
    data_superuser = {"username": company_user.username, "password": '123'}
    data_no_superuser = {"username": no_company_user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data_superuser)
        data = token_response.json()
        global company_user_access_token
        company_user_access_token = data['access_token']
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data_no_superuser)
        data = token_response.json()
        global no_company_user_access_token
        no_company_user_access_token = data['access_token']


@pytest.mark.asyncio
async def test_create_classification():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        example_value = {"name": "IT", }
        classification_response = await ac.post(
            "/api/v1/company/classification", headers={'Authorization': f'Bearer {company_user_access_token}'},
            json=example_value
        )
        assert classification_response.status_code == 200
        example_value = {"name": "Finnance", }
        await ac.post(
            "/api/v1/company/classification", json=example_value,
            headers={'Authorization': f'Bearer {company_user_access_token}'}
        )


@pytest.mark.asyncio
async def test_list_classification():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        classification_response = await ac.get("/api/v1/company/classification",
                                               headers={'Authorization': f'Bearer {company_user_access_token}'})
        assert classification_response.status_code == 200
        assert len(classification_response.json()) == 2


@pytest.mark.asyncio
async def test_create_company():
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
        assert company_response_data['classification_id'] == 1
        assert company_response_data['owner'] == {'first_name': company_user.first_name, 'id': company_user.id}
        company_response_incorrect = await ac.post(
            "/api/v1/company/", json=data, headers={'Authorization': f'Bearer {no_company_user_access_token}'}
        )
        error_meessage = {'detail': 'User does not have privileges of company'}
        assert company_response_incorrect.json() == error_meessage


@pytest.mark.asyncio
async def test_create_address():
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
async def test_list_address():
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
async def test_put_address():
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
