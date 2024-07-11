from typing import Generic, Any, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, func, select

from src.db.entities import Entity
from src.db.clients.postgres import PostgresDatabase
from src.db.repositories.abstract import (
    AbstractRepository,
    AbstractRepositoryCD,
    AbstractRepositoryCRD,
)

Model = TypeVar("Model", bound=Entity)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class InitRepository:
    def __init__(self, database: PostgresDatabase, model: type[Model]):
        self._database = database
        self._model = model


class PostgresRepositoryCD(
    InitRepository,
    AbstractRepositoryCD,
    Generic[Model, CreateSchema],
):
    async def create(self, instance: CreateSchema) -> Model:
        async with self._database.get_session() as session:
            db_obj = self._model(**instance.dict())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def remove(self, instance_uuid: UUID, **kwargs) -> UUID:
        async with self._database.get_session() as session:
            await session.execute(
                delete(self._model).where(self._model.uuid == instance_uuid)
            )
            await session.commit()
            return instance_uuid


class PostgresRepositoryCRD(
    PostgresRepositoryCD[Model, CreateSchema],
    AbstractRepositoryCRD,
    Generic[Model, CreateSchema],
):
    async def get_all(self) -> list[Model] | Any:
        async with self._database.get_session() as session:
            db_objs = await session.execute(select(self._model))
            return db_objs.scalars().all()

    async def get(self, instance_uuid: UUID, **kwargs) -> Model | Any:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(self._model).where(self._model.uuid == instance_uuid)
            )
            return db_obj.scalars().first()


class PostgresRepository(
    PostgresRepositoryCRD[Model, CreateSchema],
    AbstractRepository,
    Generic[Model, CreateSchema, UpdateSchema],
):
    async def update(self, instance_uuid: UUID, instance: UpdateSchema) -> Model:
        async with self._database.get_session() as session:
            db_obj = await self.get(instance_uuid)
            obj_data = jsonable_encoder(db_obj)
            update_data = instance.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def count(self) -> int | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(func.count()).select_from(self._model)
            )
            return db_obj.scalars().first()

    async def get_filter_by(self, **kwargs) -> Model | None:
        if not kwargs:
            raise ValueError("Filter by is empty")
        async with self._database.get_session() as session:
            db_obj = await session.execute(select(self._model).filter_by(**kwargs))
            obj = db_obj.scalars().first()
            return obj
