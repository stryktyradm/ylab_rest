import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.core.config import settings
from src.db.base import Base
from src.main import app


@pytest.fixture(scope='session')
def get_test_url(api_v: str = settings.API_V1_STR) -> dict:
    urls = {
        'menu': api_v + '/menus/{}',
        'submenu': api_v + '/menus/{}/submenus/{}',
        'dish': api_v + '/menus/{}/submenus/{}/dishes/{}'
    }
    return urls


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture(autouse=True)
async def test_db() -> AsyncSession:
    async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, future=True)
    async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with async_session() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()
