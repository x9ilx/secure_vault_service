from typing import Optional

from pydantic import BaseModel


class SecretBase(BaseModel):
    message: str
    expiration_time: int


class SecretCreate(SecretBase):
    password: str
    files: Optional[list] = []


class Secret(SecretBase):
    id: str
    creator_id: int

    class Config:
        orm_mode = True
