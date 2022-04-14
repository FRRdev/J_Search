import pytest
from httpx import AsyncClient
from main import app
from src.app.auth.security import get_password_hash
from src.app.user.models import User


@pytest.mark.asyncio
async def test_create_user():
    name, age = ["sam", 99]
    assert await User.filter(username=name).count() == 0
    password = '123'
    password_hash = get_password_hash(password)
    await User.create(
        username=name, email='test@mail.ru', password=password_hash, first_name='Samick',
        is_active=True, is_superuser=True, is_company=True
    )
    password_hash = get_password_hash(password)
    await User.create(
        username='no_active', email='noact@mail.ru', password=password_hash, first_name='ErrorUser',
        is_active=True, is_superuser=False, is_company=True
    )
    assert await User.filter(username=name).count() == 1


@pytest.mark.asyncio
async def test_admin_can_get_users():
    user = await User.get(username='sam')
    data = {"username": user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data)
        data = token_response.json()
        access_token = data['access_token']
        users_response = await ac.get("/api/v1/admin/user/", headers={'Authorization': f'Bearer {access_token}'})
        data = users_response.json()
        data_must_exist = {
            'first_name': 'Samick',
            'id': user.id,
        }
        assert data is not None
        assert data_must_exist in data


@pytest.mark.asyncio
async def test_privileges_get_users():
    user = await User.get(username='no_active')
    data = {"username": user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data)
        data = token_response.json()
        access_token = data['access_token']
        users_response = await ac.get("/api/v1/admin/user/", headers={'Authorization': f'Bearer {access_token}'})
        data = users_response.json()
        error_meessage = {'detail': 'User does not have enough privileges'}
        assert error_meessage == data


@pytest.mark.asyncio
async def test_get_single_user():
    user = await User.get(username='sam')
    data = {"username": user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data)
        data = token_response.json()
        access_token = data['access_token']
        users_response = await ac.get(
            f"/api/v1/admin/user/{user.id}", headers={'Authorization': f'Bearer {access_token}'}
        )
        data = users_response.json()
        assert data is not None
        correct_response = {
            "first_name": user.first_name,
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "is_company": user.is_company
        }
        assert data == correct_response
