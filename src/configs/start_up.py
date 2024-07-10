from pydantic import Field, SecretStr


from src.utils.settings import FastApiSettings


class StartUpSettings(FastApiSettings):
    admin_email: str = Field(..., alias="ADMIN_EMAIL")
    admin_password: SecretStr = Field(..., alias="ADMIN_PASSWORD")
