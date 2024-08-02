from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTable
)

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from app.core.db import Base


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer,
            ForeignKey("user.id", ondelete="cascade"),
            nullable=False
        )