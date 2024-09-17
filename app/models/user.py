from app.core.db import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(SQLAlchemyBaseUserTable[int], Base):
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, default='New User'
    )
    user_secrets: Mapped[list['app.models.secret.Secret']] = relationship(
        back_populates='owner',
    )
    secrets_for_users: Mapped[
        list['app.models.secret.SecretForUsers']
    ] = relationship()
