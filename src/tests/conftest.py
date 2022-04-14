import asyncio
import pytest

from tortoise import Tortoise

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


