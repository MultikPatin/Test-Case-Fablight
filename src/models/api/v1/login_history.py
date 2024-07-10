from uuid import UUID

from pydantic import BaseModel, Field

from src.models.api.v1.base import TimeMixin, UUIDMixin
from src.utils.pagination import PaginatedMixin


class RequestLoginHistory(BaseModel):
    user_uuid: UUID = Field(
        description="UUID идентификатор пользователя",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    ip_address: str = Field(
        description="IP с которого пришёл запрос логирования",
        examples=["143.098.140.003"],
    )
    user_agent: str


class LoginHistoryBase(RequestLoginHistory, UUIDMixin, TimeMixin):
    pass


class ResponseLoginHistory(LoginHistoryBase, UUIDMixin, TimeMixin):
    pass


class ResponseLoginHistoryPaginated(PaginatedMixin):
    results: list[ResponseLoginHistory]
