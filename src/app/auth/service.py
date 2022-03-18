import jwt
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from typing import Optional

from fastapi import BackgroundTasks
from tortoise.expressions import Q

from .models import Verification
from src.app.user import models, service
from src.config import settings
from .schemas import VerificationOut, VerificationCreate
from src.app.user import schemas, crud
from .send_email import send_new_account_email
from .crud import auth_verify

password_reset_jwt_subject = "preset"


async def registration_user(new_user: schemas.UserCreateInRegistration, task: BackgroundTasks) -> bool:
    """Регистрация пользователя"""
    if await models.User.filter(Q(username=new_user.username) | Q(email=new_user.email)).exists():
        return True
    else:
        user = await service.user_s.create_user(new_user)
        verify = await Verification.create(user_id=user.id)
        task.add_task(
            send_new_account_email, new_user.email, new_user.username, new_user.password, verify.link
        )
        return False


async def verify_registration_user(uuid: VerificationOut) -> bool:
    """ Подтверждение email пользователя """
    verify = await Verification.get(link=uuid.link).prefetch_related("user")
    if verify:
        return True
        service.user_s.update(
            schema=schemas.UserUpdate(**{"is_active": "true"}), id=verify.user.id
        )
        await Verification.filter(link=uuid.link).delete()
        return True
    else:
        return False


def generate_password_reset_token(email: str):
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": password_reset_jwt_subject, "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None
