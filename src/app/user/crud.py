from typing import Optional
from sqlalchemy.orm import Session
from src.app.auth.security import verify_password, get_password_hash
from src.app.base.crud_base import CRUDBase

from .models import User
from .schemas import UserCreate, UserUpdate


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[User]:
        return db_session.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, db_session: Session, *, username: str) -> Optional[User]:
        return db_session.query(self.model).filter(self.model.username == username).first()

    def get_by_username_email(self, db_session: Session, *, username: str, email: str) -> Optional[User]:
        return self.exists(db_session, username=username, email=email)

    def create(self, db_session: Session, *args, schema: UserCreate, **kwargs) -> User:
        db_obj = User(
            username=schema.username,
            email=schema.email,
            password=get_password_hash(schema.password),
            first_name=schema.first_name,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def authenticate(self, db_session: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db_session, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, obj: User) -> bool:
        return obj.is_active

    def is_superuser(self, obj: User) -> bool:
        return obj.is_superuser

    def change_password(self, db_session: Session, obj: User, hashed_password: str):
        obj.password = hashed_password
        db_session.add(user)
        db_session.commit()


user = UserCRUD(User)
