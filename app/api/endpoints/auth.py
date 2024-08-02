from fastapi.routing import APIRouter
from fastapi_users import FastAPIUsers

from app.core.user import auth_backend, get_user_manager
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
users_routers = fastapi_users.get_users_router(UserRead, UserUpdate)
users_routers.routes = [
    route
    for route in users_routers.routes
    if route.name != 'users:delete_user'
]
router.include_router(users_routers, prefix='/users', tags=['auth'])