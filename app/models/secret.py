import datetime
from typing import Optional
import argon2
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Secret(Base):
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    owner: Mapped['app.models.user.User'] = relationship(
        back_populates='user_secrets',
    )
    text: Mapped[str]
    hashed_passphrase: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
    )
    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(True),
        default=datetime.datetime.now(),
    )
    destroy_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True),
        default=None,
    )
    files: Mapped[list['SecretFiles']] = relationship(back_populates='secret',)
    secrets_for_users: Mapped[
        list['app.models.secret.SecretForUsers']
    ] = relationship()

    @staticmethod
    def hash_passphrase(passphrase: str) -> str:
        argon2.hash_password()
        return passphrase


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
    user: Mapped['app.models.user.User'] = relationship(
        back_populates='secrets_for_users',
    )
    secret: Mapped['app.models.secret.Secret'] = relationship(
        back_populates='secrets_for_users',
    )