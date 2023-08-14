import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.tests.utils import (
    create_menu,
    create_multi_submenus,
    create_submenu,
    create_submenu_data,
)


async def test_create_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    data = create_submenu_data()
    menu = await create_menu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, '')
    response = await client.post(url=url, json=data.dict())
    assert response.status_code == 201
    content = response.json()
    assert content['title'] == data.title
    assert content['description'] == data.description
    assert 'id' in content
    assert 'dishes_count' in content


async def tests_create_submenu_in_non_existent_menu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    data = create_submenu_data()
    url = get_test_url['submenu'].format(str(uuid.uuid4()), '')
    response = await client.post(url=url, json=data.dict())
    assert response.status_code == 404


async def test_get_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu = await create_submenu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, submenu.id)
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    for key, value in content.items():
        assert value == getattr(submenu, key)


async def test_get_non_existent_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, _ = await create_submenu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, str(uuid.uuid4()))
    response = await client.get(url=url)
    assert response.status_code == 404


async def test_get_list_submenus(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenus = await create_multi_submenus(db=test_db)
    url = get_test_url['submenu'].format(menu.id, '')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(submenus)
    for index, data in enumerate(content):
        for key, value in data.items():
            assert value == getattr(submenus[index], key)


async def test_update_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    update_data = create_submenu_data()
    menu, submenu = await create_submenu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, submenu.id)
    response = await client.patch(url=url, json=update_data.dict())
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == submenu.id
    assert content['dishes_count'] == submenu.dishes_count
    assert content['title'] == update_data.title
    assert content['description'] == update_data.description


async def test_update_non_existent_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    update_data = create_submenu_data()
    menu, _ = await create_submenu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, str(uuid.uuid4()))
    response = await client.patch(url=url, json=update_data.dict())
    assert response.status_code == 404


async def test_delete_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu = await create_submenu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, submenu.id)
    response = await client.delete(url=url)
    assert response.status_code == 200
    response = await client.get(url=url)
    assert response.status_code == 404


async def test_delete_non_existent_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, _ = await create_submenu(db=test_db)
    url = get_test_url['submenu'].format(menu.id, str(uuid.uuid4()))
    response = await client.get(url=url)
    assert response.status_code == 404
