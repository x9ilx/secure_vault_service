from fastapi import APIRouter

from .endpoints import secrets_router, user_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(secrets_router)
