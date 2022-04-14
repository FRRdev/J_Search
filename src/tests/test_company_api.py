import pytest
from httpx import AsyncClient
from main import app
from src.app.auth.security import get_password_hash
from src.app.user.models import User

company_user, no_company_user = User, User
company_user_access_token = None


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
    data = {"username": company_user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data)
        data = token_response.json()
        global company_user_access_token
        company_user_access_token = data['access_token']


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
