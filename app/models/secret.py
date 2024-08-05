from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Secret(Base):
    text: Mapped[str]
    hashed_passphrase: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )
    files: Mapped[list['SecretFiles']] = relationship(back_populates='secret',)
    users: Mapped[list['SecretForUsers']] = relationship(
        back_populates='current_secrets',
    )


class SecretFiles(Base):
    path: Mapped[str]
    secret_id: Mapped[int] = mapped_column(
        ForeignKey('secret.id'),
        primary_key=True,
    )
    secret: Mapped['Secret'] = relationship(back_populates='files',)


class SecretForUsers(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        primary_key=True,
    )
    secret_id: Mapped[int] = mapped_column(
        ForeignKey('secret.id'),
        primary_key=True,
    )
    secret: Mapped['User'] = relationship(back_populates='secrets',)
    secret: Mapped['Secret'] = relationship(back_populates='users',)