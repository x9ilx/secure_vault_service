from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.secret import SecretFiles, SecretForUsers


class SecretFileBase(BaseModel):
    path: str


class SecretFileCreate(SecretFileBase):
    pass


class SecretFileUpdate(SecretFileBase):
    pass


class SecretFileView(SecretFileBase):
    id: int

    class Config:
        orm_mode = True


class SecretForUsersBase(BaseModel):
    user_id: int
    


class SecretForUsersCreate(SecretForUsersBase):
    secret_id: int


class SecretForUsersUpdate(SecretForUsersBase):
    pass


class SecretForUsersView(SecretForUsersBase):
    id: int

    class Config:
        orm_mode = True


class SecretBase(BaseModel):
    owner_id: int
    text: str
    files: Optional[list[SecretFileBase]]
    for_users: Optional[list[SecretForUsersBase]]


class SecretCreate(SecretBase):
    passphrase: str


class SecretUpdate(SecretBase):
    passphrase: str

class SecretView(SecretBase):
    id: int
    create_date: datetime
    destroy_date: datetime
    files: Optional[list[SecretFileView]]
    for_users: Optional[list[SecretForUsersView]]

    class Config:
        orm_mode = True
