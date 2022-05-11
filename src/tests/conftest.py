import asyncio
import pytest

from tortoise import Tortoise
from httpx import AsyncClient
from main import app

from src.app.auth.security import get_password_hash
from src.config import settings
from src.app.user.models import User


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": settings.APPS_MODELS}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = settings.DATABASE_URI_TEST):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope='session')
@pytest.mark.asyncio
async def company_user_token():
    password = '123'
    password_hash = get_password_hash(password)
    company_user = await User.create(
        username='copmany_test', email='company2@mail.ru', password=password_hash, first_name='ComCorrect',
        is_active=True, is_superuser=True, is_company=True
    )
    data_superuser = {"username": company_user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data_superuser)
        data = token_response.json()
        company_user_access_token = data['access_token']
    return company_user, company_user_access_token


@pytest.fixture(scope='session')
@pytest.mark.asyncio
async def no_company_user_token():
    password = '123'
    password_hash = get_password_hash(password)
    no_company_user = await User.create(
        username='no_active_another', email='noact2@mail.ru', password=password_hash, first_name='ErrorUser2',
        is_active=True, is_superuser=False, is_company=False
    )
    data_no_superuser = {"username": no_company_user.username, "password": '123'}
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        token_response = await ac.post("/api/v1/auth/login/access-token", data=data_no_superuser)
        data = token_response.json()
        no_company_user_access_token = data['access_token']
    return no_company_user, no_company_user_access_token
