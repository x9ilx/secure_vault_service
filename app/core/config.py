from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class AppConfig(BaseModel):
    app_title: str = (
        'Сервис защищенного обмена сообщениями и файлами в сети организации'
    )
    app_description: str = (
        'Сервис позволяет назначить время жизни сообщению, а так же '
        'назначить секретную фразу (пароль), для доступа к сообщению. '
        'Сообщения без секретной фразы (пароля) общедоступны и их могут '
        'Просматривать все авторизованные пользователи.'
    )


class DBConfig(BaseModel):
    database_url: str = None
    echo: bool = False
    echo_pool: bool = False
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


class SecurityConfig(BaseModel):
    secret: str = 'YOUR_SECRET_KEY'
    jwt_lifetime: int = 3500


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = '../.env',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    app: AppConfig = AppConfig()
    db: DBConfig = DBConfig()
    security: SecurityConfig = SecurityConfig()


settings = Settings()
