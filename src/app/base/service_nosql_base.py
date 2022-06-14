from typing import TypeVar, Type, Optional, List, Any
from collections import ChainMap

from motor.core import Collection
from pydantic import BaseModel

CollectionType = TypeVar("CollectionType", bound=Collection)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)


class BaseService:
    collection: Type[CollectionType]

    async def all(self) -> List:
        cursor = self.collection.find()
        items = await cursor.to_list(length=500)
        return items

    async def create(self, schema: CreateSchemaType, *args, **kwargs):
        data_to_insert = ChainMap(schema.dict(), kwargs)
        inserted_obj = await self.collection.insert_one(data_to_insert)
        obj = await self.collection.find_one({"_id": inserted_obj.inserted_id})
        return obj
