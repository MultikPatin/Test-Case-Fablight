from src.configs.postgres import PostgresSettings
from src.configs.redis import RedisSettings
from src.configs.token import TokenSettings
from src.configs.start_up import StartUpSettings

from src.utils.settings import EnvSettings, FastApiSettings

__all__ = [
    "settings",
    "LOGGING",
    "PostgresSettings",
    "StartUpSettings",
    "TokenSettings",
    "RedisSettings",
]


class AppSettings(FastApiSettings):
    pass


class Settings(EnvSettings):
    app: AppSettings = AppSettings()
    start_up: StartUpSettings = StartUpSettings()
    token: TokenSettings = TokenSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()

if not settings.start_up.migrations:
    from logging import config as logging_config

    from src.configs.logger import LOGGING
    from async_fastapi_jwt_auth import AuthJWT

    logging_config.dictConfig(LOGGING)


    @AuthJWT.load_config
    def get_config():
        return Settings().token

if settings.app.debug:
    print(settings.model_dump())
