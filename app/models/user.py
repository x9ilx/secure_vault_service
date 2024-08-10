from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_secrets: Mapped[list['app.models.secret.Secret']] = relationship(
        back_populates='owner',
    )
    secrets_for_users: Mapped[
        list['app.models.secret.SecretForUsers']
    ] = relationship()