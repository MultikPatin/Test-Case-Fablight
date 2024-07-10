import uuid
from typing import TYPE_CHECKING

from pydantic import SecretStr
from sqlalchemy import Boolean, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from src.db.entities import Entity

if TYPE_CHECKING:
    from src.db.entities import LoginHistory


class User(Entity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default=false())

    login_history: Mapped[list["LoginHistory"]] = relationship(
        "LoginHistory",
        back_populates="user",
        cascade="all, delete",
        order_by="LoginHistory.created_at.desc()",
    )

    def __init__(
            self,
            email: str,
            password: SecretStr,
            first_name: str,
            last_name: str,
            role_uuid: uuid.UUID,
            is_superuser: bool = False,
    ) -> None:
        self.email = email
        self.password = generate_password_hash(password.get_secret_value())
        self.first_name = first_name
        self.last_name = last_name
        self.role_uuid = role_uuid
        self.is_superuser = is_superuser

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
