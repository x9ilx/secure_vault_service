from fastapi import APIRouter, Depends
from app.schemas import secret
from app.crud import secret as crud_secret
from app.api.dependencies import get_current_user

router = APIRouter()
