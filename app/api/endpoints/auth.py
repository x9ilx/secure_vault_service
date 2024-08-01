from fastapi import APIRouter, Depends
from app.schemas import user, token
from app.core import security
from app.crud import user as crud_user

router = APIRouter()

@router.post("/login", response_model=token.Token)
def login(user_credentials: user.UserLogin):
    # логика авторизации пользователя и генерация токена
    pass

@router.post("/register", response_model=user.User)
def register(new_user: user.UserCreate):
    # логика регистрации нового пользователя
    pass
