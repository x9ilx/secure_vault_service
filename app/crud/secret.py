from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.secret import Secret
from app.schemas.secret import SecretCreate, SecretUpdate
from app.models.user import User


class SecretCrud():

    @classmethod
    async def get(
        cls,
        obj_id: int,
        passphrase: str,
        user: User,
        session: AsyncSession,
    ) -> Secret | None:
        hashed_passphrase = Secret.hash_passphrase(passphrase)
        db_obj = session.execute(
            select(Secret)
            .where(
                Secret.id == obj_id,
                or_(
                    Secret.hashed_passphrase == hashed_passphrase,
                    user.id in Secret.for_users,
                    user.id == Secret.owner_id,
                )
            )
        )
        return db_obj.scalars().first()

    @classmethod
    async def get_all_for_owner(
        cls,
        user: User,
        session: AsyncSession,
    ) -> list[Secret] | None:
        db_objs = await session.execute(
            select(Secret)
            .where(Secret.owner_id == user.id)
        )
        return db_objs.scalars().all()

    @classmethod
    async def get_all_public_secrets(
        cls,
        session: AsyncSession,
    ) -> list[Secret] | None:
        db_objs = await session.execute(
            select(Secret)
            .where(Secret.hashed_passphrase is None)
        )
        return db_objs.scalars().all()

    @classmethod
    async def create(
        obj_in: SecretCreate,
        user: User,
        session: AsyncSession,
        
    ) -> Optional[Secret]:
        db_obj = Secret(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @classmethod
    async def update(
        self,
        db_obj: Secret,
        obj_in: SecretUpdate,
        session: AsyncSession,
    ) -> Optional[Secret]:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @classmethod
    async def delete(
        self,
        db_obj: Secret,
        session: AsyncSession
    ) -> Secret:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
