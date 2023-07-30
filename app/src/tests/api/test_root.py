from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session


def test_root(client: TestClient, get_db: Session):
    db_tables = ['menu', 'submenu', 'dish']
    test_query = text(
        "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    )
    row = get_db.execute(test_query)
    response = client.get("/")
    assert response.status_code == 200
    for table_name in row.fetchall():
        assert table_name[0] in db_tables
