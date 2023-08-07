import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator

BASEDIR: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
)
load_dotenv(os.path.join(BASEDIR, '.env'))


class Settings(BaseSettings):

    # Main project settings.
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str

    # DB/Postgres settings.
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER', default='localhost')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', default='5432')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', default='postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', default='pass')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', default='app')
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None

    # Cache/Redis settings.
    REDIS_HOST: str = os.getenv('REDIS_HOST', default='localhost')
    REDIS_PORT: str = os.getenv('REDIS_PORT', default='6379')
    REDIS_CACHE_TIME: str | int = os.getenv('REDIS_CACHE_TIME', default=3600)
    REDIS_URI: RedisDsn | None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER', 'postgres'),
            password=values.get('POSTGRES_PASSWORD', 'pass'),
            host=values.get('POSTGRES_SERVER', 'localhost'),
            port=values.get('POSTGRES_PORT', '5432'),
            path=f"/{values.get('POSTGRES_DB') or ''}"
        )

    @validator('REDIS_URI', pre=True)
    def assemble_redis_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme='redis',
            host=values.get('REDIS_HOST', 'localhost'),
            port=values.get('REDIS_PORT', '6379')
        )

    class Config:
        case_sensitive = True


settings = Settings()
