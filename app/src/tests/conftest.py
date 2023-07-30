from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.core.config import settings
from src.db.base import Base
from src.main import app


@pytest.fixture(scope="session")
def get_test_url(api_v: str = settings.API_V1_STR) -> dict:
    urls = {
        "menu": api_v + "/menus/{}",
        "submenu": api_v + "/menus/{}/submenus/{}",
        "dish": api_v + "/menus/{}/submenus/{}/dishes/{}"
    }
    return urls


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as t_client:
        yield t_client


@pytest.fixture(autouse=True)
def get_db_override() -> None:
    def get_test_db() -> Generator:
        yield get_db

    app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(autouse=True)
def reset_dependency_overrides() -> Generator:
    yield
    app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def get_db() -> Session:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with testing_session() as session:
        Base.metadata.create_all(engine)
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()
