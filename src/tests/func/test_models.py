import pytest
from src.app.auth.security import get_password_hash
from src.app.user.models import User


@pytest.mark.asyncio
async def test_create_users():
    password = 'qwerty'
    username_list = ['admin', 'IvCOmpany', 'FRRdev', 'IvanNoAct']
    passwords_hash = [get_password_hash(password) for _ in range(4)]
    await User.create(
        username='admin', email='admin@mail.ru', password=passwords_hash[0],
        first_name='Admin', is_active=True, is_superuser=True, is_company=True
    )
    await User.create(
        username='IvCOmpany', email='company@mail.ru', password=passwords_hash[1],
        first_name='IvComp', is_active=True, is_superuser=False, is_company=True
    )
    await User.create(
        username='FRRdev', email='mixail@mail.ru', password=passwords_hash[2],
        first_name='Mikhail', is_active=True, is_superuser=False, is_company=False
    )
    await User.create(
        username='IvanNoAct', email='ivan@mail.ru', password=passwords_hash[3],
        first_name='IvanNoAct', is_active=False, is_superuser=False, is_company=False
    )
    assert await User.filter(username__in=username_list).count() == 4
