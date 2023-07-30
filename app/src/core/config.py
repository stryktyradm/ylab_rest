import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator

BASEDIR: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
)
load_dotenv(os.path.join(BASEDIR, ".env"))


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", default="localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", default="pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", default="app")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER", "postgres"),
            password=values.get("POSTGRES_PASSWORD", "pass"),
            host=values.get("POSTGRES_SERVER", "localhost"),
            path=f"/{values.get('POSTGRES_DB') or ''}"
        )

    class Config:
        case_sensitive = True


settings = Settings()
