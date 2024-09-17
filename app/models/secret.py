import datetime
from typing import Optional

from app.core.db import Base
from argon2 import PasswordHasher
from sqlalchemy import DateTime, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
    lifetime: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('lifetime >= 60', name='secret_lifetime_min_value'),
    )
    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(True),
        default=datetime.datetime.now(),
    )
    destroy_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(True),
    )
    files: Mapped[list['SecretFiles']] = relationship(
        'SecretFiles', back_populates='secret'
    )
    secrets_for_users: Mapped[list['SecretForUsers']] = relationship(
        'SecretForUsers', back_populates='secret'
    )

    @staticmethod
    def hash_passphrase(passphrase: str) -> str:
        password_hasher = PasswordHasher()
        return password_hasher.hash(passphrase)

    @staticmethod
    def verify_passphrase(passphrase: str, obj_hash: str):
        password_hasher = PasswordHasher()
        return password_hasher.verify(obj_hash, passphrase)


class SecretFiles(Base):
    path: Mapped[str]
    secret_id: Mapped[int] = mapped_column(
        ForeignKey('secret.id'),
        primary_key=True,
    )
    secret: Mapped['Secret'] = relationship('Secret', back_populates='files')


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
        'User',
        back_populates='secrets_for_users',
    )
    secret: Mapped['app.models.secret.Secret'] = relationship(
        'Secret',
        back_populates='secrets_for_users',
    )
