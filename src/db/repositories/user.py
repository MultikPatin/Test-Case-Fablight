from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from src.models.api.v1.users import RequestUserCreate, RequestUserUpdate
from src.models.api.v1.users_additional import RequestPasswordChange
from src.db.clients.postgres import (
    PostgresDatabase,
    get_postgres_db,
)
from src.db.entities import User
from src.db.repositories.base import PostgresRepository


class UserRepository(
    PostgresRepository[User, RequestUserCreate, RequestUserUpdate],
):

    async def change_password(
            self, user_uuid: UUID, obj: RequestPasswordChange
    ) -> User | None:
        async with self._database.get_session() as session:
            user = await self.get(user_uuid)
            if user.check_password(obj.current_password.get_secret_value()):
                user.password = obj.new_password.get_secret_value()
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            return None


@lru_cache
def get_user_repository(
        database: PostgresDatabase = Depends(get_postgres_db),
) -> UserRepository:
    return UserRepository(database, User)
