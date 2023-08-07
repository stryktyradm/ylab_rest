from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_root(client: AsyncClient):
    response = await client.get(url='/')
    assert response.status_code == 200


async def test_present_tables(test_db: AsyncSession):
    db_tables = ['menu', 'submenu', 'dish']
    test_query = text(
        "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    )
    rows = await test_db.execute(test_query)
    fetched_tables = [row[0] for row in rows.fetchall()]
    for table_name in db_tables:
        assert table_name in fetched_tables
