import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Base
from src.db.session import async_engine, async_session


@pytest.fixture(scope='module')
def ids() -> dict[str, str]:
    id_s = {
        'menu': '',
        'submenu': '',
        'dish': '',
        'dish_2': '',
    }
    return id_s


@pytest_asyncio.fixture(scope='module', autouse=True)
async def test_db() -> AsyncSession:
    async with async_session() as session:

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()
