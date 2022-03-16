from typing import TypeVar, Type, Optional, Generic, List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def exists(self, db_session: Session, **kwargs):
        return db_session.query(
            db_session.query(self.model.id).filter_by(**kwargs).exists()
        ).scalar()

    def get_object_or_404(self, db_session: Session, id: int) -> Optional[ModelType]:
        pass

    def get(self, db_session: Session, **kwargs) -> Optional[ModelType]:
        return db_session.query(self.model).filter_by(**kwargs).first()

    def all(self, db_session: Session, *args, skip=0, limit=100) -> List[ModelType]:
        return db_session.query(self.model).offset(skip).limit(limit).all()

    def filter(self, db_session: Session, *args, **kwargs) -> List[ModelType]:
        return db_session.query(self.model).filter_by(**kwargs)

    def create(self, db_session: Session, *args, schema: CreateSchemaType, **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(schema)
        db_obj = self.model(**obj_in_data, **kwargs)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: Session, *args, model: ModelType, schema: UpdateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(model)
        update_data = schema.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(model, field, update_data[field])
        db_session.add(model)
        db_session.commit()
        db_session.refresh(model)
        return model

    def remove(self, db_session: Session, *args, **kwargs) -> ModelType:
        obj = self.get(db_session, **kwargs)
        db_session.delete(obj)
        db_session.commit()
        return obj
