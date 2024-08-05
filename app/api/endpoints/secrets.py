from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.db import get_async_session
from app.crud import secret as crud_secret
from app.schemas import secret

router = APIRouter()


@router.get(
    '/',
    response_model=list[None],
)
async def get_all_public_secrets(
    session: AsyncSession = Depends(get_async_session),
):
    pass
