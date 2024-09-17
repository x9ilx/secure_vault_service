from fastapi import APIRouter
from app.core.db import get_async_session
from app.crud.secret import SecretCrud


router = APIRouter()


async def deactivate_secrets():
    session = get_async_session()
    secrets = await SecretCrud.get_all_overdue_secrets(session)
    print(secrets)
    await SecretCrud.deactivate_overdue_secrets(secrets, session)