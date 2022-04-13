import pytest
from httpx import AsyncClient
from main import app
from src.app.auth.security import get_password_hash
from src.app.user.models import User


@pytest.mark.asyncio
async def test_testpost():
    name, age = ["sam", 99]
    assert await User.filter(username=name).count() == 0
    password = '123'
    password_hash = get_password_hash(password)
    await User.create(username=name, email='test@mail.ru', password=password_hash, first_name='Samick', is_active=True,
                      is_superuser=True, is_company=True)
    assert await User.filter(username=name).count() == 1
    data = {"username": name, "password": password}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("/api/v1/auth/login/access-token", data=data)
        data = response.json()
        access_token = data['access_token']
        assert access_token is not None
