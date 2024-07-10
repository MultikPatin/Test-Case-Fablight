from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

from src.db.repositories.abstract import AbstractRepository

Schema = TypeVar("Schema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class InitService:
    def __init__(self, repository: AbstractRepository, model: type[Schema]):
        self._repository = repository
        self._model = model


class BaseServiceCD(
    InitService,
    Generic[Schema, CreateSchema],
):
    async def create(self, obj: CreateSchema) -> Schema:
        obj = await self._repository.create(obj)
        return self._model.model_validate(obj, from_attributes=True)

    async def remove(self, obj_uuid: UUID) -> UUID:
        return await self._repository.remove(obj_uuid)


class BaseServiceCRD(
    BaseServiceCD[Schema, CreateSchema],
    Generic[Schema, CreateSchema],
):
    async def get(self, instance_uuid: UUID) -> Schema | None:
        obj = await self._repository.get(instance_uuid)
        if obj is None:
            return None
        return self._model.model_validate(obj, from_attributes=True)

    async def get_all(self) -> list[Schema] | None:
        objs = await self._repository.get_all()
        if objs is None:
            return None
        return [self._model.model_validate(obj, from_attributes=True) for obj in objs]


class BaseService(
    BaseServiceCRD[Schema, CreateSchema],
    Generic[Schema, CreateSchema, UpdateSchema],
):
    async def update(self, obj_uuid: UUID, obj: UpdateSchema) -> Schema:
        obj = await self._repository.update(obj_uuid, obj)
        return self._model.model_validate(obj, from_attributes=True)

    async def count(self) -> int | None:
        return await self._repository.count()
