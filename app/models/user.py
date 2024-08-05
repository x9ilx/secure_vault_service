from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    users: Mapped[list['SecretForUsers']] = relationship(
        back_populates='for_users',
    )
