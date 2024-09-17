from pathlib import Path
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    app_title: str = (
        (
            'Secure messaging and file sharing service on the organization\'s '
            'network'
        )
    )
    app_description: str = (
        'The service allows you to assign a lifetime to a message, as well as '
        'assign a secret phrase (password) to access the message. '
        'Messages without a secret phrase (password) are publicly available '
        'and can be viewed by all authorized users.'
    )
    base_dir_for_files: Path = Path('files/')
    chunk_size: int = 1024


class DBConfig(BaseModel):
    database_url: str = None
    sheduler_database_url: str = None
    echo: bool = False
    echo_pool: bool = False
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


class SecurityConfig(BaseModel):
    secret: str = 'YOUR_SECRET_KEY'
    jwt_lifetime: int = 3500


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='app/.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    app: AppConfig = AppConfig()
    db: DBConfig = DBConfig()
    security: SecurityConfig = SecurityConfig()


settings = Settings()


def create_dirs():
    results_dir = Path(settings.app.base_dir_for_files)
    results_dir.mkdir(exist_ok=True)


create_dirs()
