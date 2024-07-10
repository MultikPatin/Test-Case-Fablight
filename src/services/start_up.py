import logging

from sqlalchemy import select

from src.configs import StartUpSettings
from src.models.api.v1.users import RequestUserCreate
from src.db.clients.postgres import PostgresDatabase
from src.db.entities import User

logger = logging.getLogger("StartUpService")


class StartUpService:
    def __init__(self, database: PostgresDatabase, settings: StartUpSettings):
        self.__database = database
        self.__settings = settings

    async def create_admin_user(self) -> None:
        user_uuid = await self.get_uuid_by_email(self.__settings.admin_email)
        if user_uuid:
            return
        logger.info("User with email %s already exist", self.__settings.admin_email)
        await self.create_user(
            RequestUserCreate(
                email=self.__settings.admin_email,
                password=self.__settings.admin_password,
                first_name=None,
                last_name=None,
            )
        )
        logger.info("Created admin user with email %s", self.__settings.admin_email)

    async def get_uuid_by_email(self, email: str) -> str | None:
        async with self.__database.get_session() as session:
            db_obj = await session.execute(select(User.uuid).filter_by(email=email))
            obj_uuid = db_obj.scalars().first()
            return obj_uuid

    async def create_user(self, instance: RequestUserCreate) -> None:
        async with self.__database.get_session() as session:
            role_uuid = await self.get_uuid_by_name(self.__settings.empty_role_name)
            instance_dict = instance.dict()
            instance_dict["is_superuser"] = True
            instance_dict["role_uuid"] = role_uuid
            db_obj = User(**instance_dict)
            session.add(db_obj)
            await session.commit()
