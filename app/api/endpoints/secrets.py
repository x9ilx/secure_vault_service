import aiofiles
from app.api.validators import (check_file_exist,
                                check_secret_exist_and_avaliable,
                                verify_passphrase)
from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.secret import SecretCrud
from app.models.user import User
from app.schemas.secret import (SecretCreate, SecretGetFile, SecretView,
                                SecretViewForUser)
from fastapi import APIRouter, Body, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/secrets', tags=['secrets'])


@router.get(
    '/all_public',
    response_model=list[SecretViewForUser],
    summary='Obtaining all public secrets (no passphrase)',
)
async def get_all_public_secrets(
    session: AsyncSession = Depends(get_async_session),
):
    return await SecretCrud.get_all_public_secrets(session)


@router.post(
    '/{secret_id}/get_file',
    summary='Retrieving a file from a secret',
    description=(
        'If the secret does not have a passphrase, pass Null (None), you must '
        'also pass the file name'
    ),
)
async def get_file_from_secret(
    secret_id: int,
    secret_get_file: SecretGetFile,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    secret = await check_secret_exist_and_avaliable(
        secret_id=secret_id,
        user_db=user,
        session=session,
        passphrase=secret_get_file.passphrase,
    )
    verify_passphrase(secret, secret_get_file.passphrase)
    file_path = settings.app.base_dir_for_files / secret_get_file.file_name
    check_file_exist(file_path)
    return FileResponse(file_path)


@router.post(
    '/{secret_id}',
    response_model=SecretView,
    summary='Get the secret',
    description=(
        'The secret will be obtained if it is requested by the author, if the '
        'user is in the for_user list, if the passphrase is specified '
        'correctly, if there is no passphrase for the secret (it is public).'
        'In the body of the request, pass passphrase.'
    ),
)
async def get_secret(
    secret_id: int,
    passphrase: str
    | None = Body(
        None,
    ),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    secret = await SecretCrud.get(secret_id, passphrase, user, session)
    verify_passphrase(secret, passphrase)
    return secret


@router.post(
    '/{secret_id}/update_files',
    response_model=SecretView,
    summary='Modify files in a secret',
    description=(
        'Allows the author of a secret to change the files that are attached '
        'to it.'
    ),
)
async def update_files(
    secret_id: int,
    files: list[UploadFile],
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    secret = await check_secret_exist_and_avaliable(
        secret_id=secret_id, user_db=user, session=session
    )
    file_list = []
    try:
        if files:
            for file in files:
                file_path = (
                    settings.app.base_dir_for_files
                    / f'{user.email}_{file.filename}'
                )
                async with aiofiles.open(file_path, 'w+b') as out_file:
                    while content := await file.read(settings.app.chunk_size):
                        await out_file.write(content)
                    file_list.append(f'{user.email}_{file.filename}')
    except Exception as e:
        return {'message': e.args}
    return await SecretCrud.update_files(
        db_obj=secret, files=file_list, session=session
    )


@router.post(
    '/',
    response_model=SecretView,
    summary='Creating a secret',
    description=(
        "In case you don't want to specify specific users to view the "
        'message - leave for_user: []. Passphrase can be Null (None).'
    ),
)
async def create_secret(
    secret: SecretCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await SecretCrud.create(obj_in=secret, user=user, session=session)
