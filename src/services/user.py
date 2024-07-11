from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from src.models.api.v1 import (
    RequestUserCreate,
    RequestUserUpdate,
)
from src.models.api.v1.users_additional import RequestPasswordChange
from src.models.db.user import UserDB
from src.services.base import BaseService
from src.db.repositories.user import UserRepository, get_user_repository


class UserService(
    BaseService[
        UserDB,
        RequestUserCreate,
        RequestUserUpdate,
    ]
):
    _repository: UserRepository

    async def change_password(
            self, user_uuid: UUID, obj: RequestPasswordChange
    ) -> UserDB | None:
        obj = await self._repository.change_password(user_uuid, obj)
        if obj is not None:
            return self._model.model_validate(obj, from_attributes=True)
        return None


@lru_cache
def get_user_service(
        repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository, UserDB)
