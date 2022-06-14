import datetime
from typing import Optional

from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, Field


class PyObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not BsonObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return BsonObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CreateNote(BaseModel):
    title: str
    description: str
    deadline: datetime.datetime
    created_at: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "title": "string",
                "description": "string",
                "deadline": "2020-10-18 15:26:17",
            }
        }


class GetNote(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: Optional[int]
    description: str
    deadline: datetime.datetime
    created_at: Optional[datetime.datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {BsonObjectId: str}
