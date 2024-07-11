from pydantic import BaseModel, Field, SecretStr



class RequestPasswordChange(BaseModel):
    new_password: SecretStr = Field(
        description="Новый пароль пользователя",
        examples=["[2/#&/%M9:aOIzJ-Xb.0Ncod?HoQih"],
        min_length=1,
        max_length=255,
    )
    current_password: SecretStr = Field(
        description="Текущий пароль пользователя",
        examples=["DJVkw6U&}b;q#V-D!7^;zl?52im2*B"],
        min_length=1,
        max_length=255,
    )
