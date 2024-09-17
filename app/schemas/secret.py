from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SecretFileBase(BaseModel):
    id: int
    path: str


class SecretFileView(SecretFileBase):
    class Config:
        from_attributes = True


class SecretForUsersBase(BaseModel):
    id: int
    user_id: int


class SecretForUsersView(SecretForUsersBase):
    class Config:
        from_attributes = True


class SecretBase(BaseModel):
    text: str
    lifetime: int = Field(..., ge=60)


class SecretCreate(SecretBase):
    passphrase: Optional[str] = Field(None)
    for_users: list[int]


class SecretUpdate(SecretCreate):
    files: Optional[list[SecretFileBase]]
    for_users: Optional[SecretForUsersBase]


class SecretView(SecretBase):
    id: int
    owner_id: int
    create_date: datetime
    destroy_date: datetime
    files: list[SecretFileView] = []
    secrets_for_users: list[SecretForUsersView] = []

    class Config:
        from_attributes = True


class SecretGetFile(BaseModel):
    file_name: str
    passphrase: Optional[str] = Field(None)


class SecretViewForUser(SecretBase):
    id: int
    owner_id: int
    create_date: datetime
    destroy_date: datetime
    files: list[SecretFileView] = []

    class Config:
        from_attributes = True
