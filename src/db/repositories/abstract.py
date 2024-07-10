from abc import ABC, abstractmethod
from typing import TypeVar, Any
from uuid import UUID

from pydantic import BaseModel
from src.db.entities import Entity

Model = TypeVar("Model", bound=Entity)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class AbstractRepositoryCD(ABC):
    @abstractmethod
    async def create(self, instance: CreateSchema) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, instance_uuid: UUID) -> UUID:
        raise NotImplementedError


class AbstractRepositoryCRD(AbstractRepositoryCD, ABC):
    @abstractmethod
    async def get_all(self) -> list[Model] | Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self, instance_uuid: UUID, **kwargs) -> Model | Any:
        raise NotImplementedError


class AbstractRepository(AbstractRepositoryCRD, ABC):
    @abstractmethod
    async def update(self, instance_uuid: UUID, instance: UpdateSchema) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def get_uuid_filter_by(self, **kwargs) -> str | None:
        raise NotImplementedError
