import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

from src.config import settings
from .jwt import ALGORITHM

from .schemas import TokenPayload
from src.app.user import service
from ..user.models import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)):
    """ Check auth user
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await service.user_s.get_obj(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


def get_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="User does not have enough privileges")
    return current_user

