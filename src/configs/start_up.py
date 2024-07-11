from pydantic import Field, SecretStr


from src.utils.settings import FastApiSettings


class StartUpSettings(FastApiSettings):
    migrations: bool = Field(default=False)
    admin_email: str = Field(..., alias="ADMIN_EMAIL")
    admin_password: SecretStr = Field(..., alias="ADMIN_PASSWORD")
