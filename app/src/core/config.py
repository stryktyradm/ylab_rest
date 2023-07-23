from typing import Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
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
