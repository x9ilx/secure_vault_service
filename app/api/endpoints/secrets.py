from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.secret import SecretCrud
from app.schemas.secret import SecretView
from app.models.user import User
from app.core.user import get_user_db

router = APIRouter(
    prefix='/secrets',
    tags=['secrets']
)


@router.get(
    '/all_public',
    response_model=list[SecretView],
)
async def get_all_public_secrets(
    session: AsyncSession = Depends(get_async_session),
):
    return SecretCrud.get_all_public_secrets(session)


@router.post(
    '/',
    response_model=SecretView,
)
async def get_secret(
    secret_id: int,
    passphrase: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_user_db)
):
    return SecretCrud.get(secret_id, passphrase, user, session)