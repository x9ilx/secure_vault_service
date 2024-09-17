import os
from http import HTTPStatus
from typing import Optional

from app.core.user import current_user
from app.crud.secret import SecretCrud
from app.models.secret import Secret
from app.models.user import User
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException
from fastapi.exceptions import ResponseValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def check_secret_exist_and_avaliable(
    secret_id: int,
    user_db: User,
    session: AsyncSession,
    passphrase: str = None,
) -> Optional[Secret]:
    secret = await SecretCrud.get(
        obj_id=secret_id, passphrase=passphrase, user=user_db, session=session
    )
    print(secret.id)
    if secret is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='The message is unavailable or does not exist',
        )
    return secret


def check_file_exist(filepath: str) -> None:
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The requested file was not found',
        )


def verify_passphrase(secret: Secret, passphrase: str) -> None:
    try:
        if secret.hashed_passphrase is not None:
            Secret.verify_passphrase(
                passphrase or '', secret.hashed_passphrase
            )
    except VerifyMismatchError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The wrong passphrase',
        )
