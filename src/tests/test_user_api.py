import pytest
from httpx import AsyncClient
from main import app
from src.app.auth.security import get_password_hash
from src.app.user.models import User

superuser, no_superuser = User, User
superuser_access_token, no_superuser_access_token = None, None


@pytest.mark.asyncio
async def test_create_user():
    password = '123'
    password_hash = get_password_hash(password)
    global superuser
    superuser = await User.create(
        username='sam', email='test@mail.ru', password=password_hash, first_name='Samick',
        is_active=True, is_superuser=True, is_company=True
    )
    password_hash = get_password_hash(password)
    global no_superuser
    no_superuser = await User.create(
        username='no_active', email='noact@mail.ru', password=password_hash, first_name='ErrorUser',
        is_active=True, is_superuser=False, is_company=True
    )
    data_superuser = {"username": superuser.username, "password": '123'}
    data_no_superuser = {"username": no_superuser.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data_superuser)
        data = token_response.json()
        global superuser_access_token
        superuser_access_token = data['access_token']
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data_no_superuser)
        data = token_response.json()
        global no_superuser_access_token
        no_superuser_access_token = data['access_token']


@pytest.mark.asyncio
async def test_admin_can_get_users():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        users_response = await ac.get("/api/v1/admin/user/",
                                      headers={'Authorization': f'Bearer {superuser_access_token}'})
        data = users_response.json()
        data_must_exist = {
            'first_name': 'Samick',
            'id': superuser.id,
        }
        assert data is not None
        assert data_must_exist in data


@pytest.mark.asyncio
async def test_privileges_get_users():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        users_response = await ac.get("/api/v1/admin/user/",
                                      headers={'Authorization': f'Bearer {no_superuser_access_token}'})
        data = users_response.json()
        error_meessage = {'detail': 'User does not have enough privileges'}
        assert error_meessage == data


@pytest.mark.asyncio
async def test_get_single_user():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        users_response = await ac.get(
            f"/api/v1/admin/user/{superuser.id}", headers={'Authorization': f'Bearer {superuser_access_token}'}
        )
        data = users_response.json()
        assert data is not None
        correct_response = {
            "first_name": superuser.first_name,
            "id": superuser.id,
            "username": superuser.username,
            "email": superuser.email,
            "is_active": superuser.is_active,
            "is_superuser": superuser.is_superuser,
            "is_company": superuser.is_company
        }
        assert data == correct_response
