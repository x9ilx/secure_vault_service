import datetime
from typing import Optional

from app.models.secret import Secret, SecretFiles, SecretForUsers
from app.models.user import User
from app.schemas.secret import SecretCreate, SecretUpdate
from argon2.exceptions import VerificationError
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SecretCrud:
    @classmethod
    async def __get_refresh_object(
        cls, obj_id: int, session: AsyncSession
    ) -> Secret:
        obj_db = await session.execute(
            select(Secret)
            .options(
                joinedload(Secret.files), joinedload(Secret.secrets_for_users)
            )
            .where(Secret.id == obj_id)
        )
        return obj_db.unique().scalars().first()

    @classmethod
    async def get(
        cls,
        obj_id: int,
        passphrase: str,
        user: User,
        session: AsyncSession,
    ) -> Secret | None:
        conditions = []
        conditions.append(
            or_(
                Secret.secrets_for_users.any(user_id=user.id),
                Secret.owner_id == user.id,
                Secret.hashed_passphrase == None,
            )
        )
        db_obj = await session.execute(
            select(Secret)
            .options(
                joinedload(Secret.files), joinedload(Secret.secrets_for_users)
            )
            .where(Secret.id == obj_id, or_(*conditions))
        )
        db_obj = db_obj.unique().scalars().first()
        return db_obj

    @classmethod
    async def get_all_for_owner(
        cls,
        user: User,
        session: AsyncSession,
    ) -> list[Secret] | None:
        db_objs = await session.execute(
            select(Secret).where(Secret.owner_id == user.id)
        )
        return db_objs.unique().scalars().all()

    @classmethod
    async def get_all_public_secrets(
        cls,
        session: AsyncSession,
    ) -> list[Secret] | None:
        db_objs = await session.execute(
            select(Secret)
            .options(
                joinedload(Secret.files), joinedload(Secret.secrets_for_users)
            )
            .where(Secret.hashed_passphrase == None)
        )
        return db_objs.unique().scalars().all()

    @classmethod
    async def create(
        cls,
        obj_in: SecretCreate,
        user: User,
        session: AsyncSession,
    ) -> Optional[Secret]:
        obj_in_data = obj_in.model_dump()
        for_users = obj_in_data.pop('for_users')
        passphrase = obj_in_data.pop('passphrase')
        hashed_passphrase = (
            Secret.hash_passphrase(passphrase) if passphrase else None
        )
        db_obj = Secret(
            hashed_passphrase=hashed_passphrase,
            owner_id=user.id,
            create_date=datetime.datetime.now(),
            **obj_in_data,
        )
        db_obj.destroy_date = db_obj.create_date + datetime.timedelta(
            seconds=db_obj.lifetime
        )
        db_obj.secrets_for_users.extend(
            [SecretForUsers(user_id=user_id) for user_id in for_users]
        )
        session.add(db_obj)
        await session.commit()
        return await cls.__get_refresh_object(db_obj.id, session)

    @classmethod
    async def update(
        cls,
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
    async def delete(cls, db_obj: Secret, session: AsyncSession) -> Secret:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @classmethod
    async def update_files(
        cls, db_obj: Secret, files: list[str], session: AsyncSession
    ) -> Secret:
        existing_files = {file.path for file in db_obj.files}
        new_files = set(files)
        files_to_remove = existing_files - new_files
        for file in db_obj.files:
            if file.path in files_to_remove:
                await session.delete(file)
        db_obj.files.extend(
            [
                SecretFiles(path=file, secret_id=db_obj.id)
                for file in new_files - existing_files
            ]
        )
        session.add(db_obj)
        await session.commit()
        return await cls.__get_refresh_object(db_obj.id, session)

    @classmethod
    async def get_all_overdue_secrets(
        cls,
        session: AsyncSession
    ) -> list[Secret]:
        db_objs = await session.execute(
            select(Secret)
            .where(Secret.destroy_date <= datetime.datetime.now())
        )
        return db_objs.scalars().all()

    @classmethod
    async def deactivate_overdue_secrets(
        cls,
        secrets: list[Secret],
        session: AsyncSession
    ) -> list[Secret]:
        ...