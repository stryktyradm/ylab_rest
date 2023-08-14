import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.tests.utils import (
    create_menu,
    create_menu_data,
    create_menu_with_nested_data,
    create_multi_menus,
)


async def test_menu_with_nested_object(
    client: AsyncClient, get_test_url: dict[str, str], test_db: AsyncSession
):
    all_menus = await create_menu_with_nested_data(db=test_db)
    url = get_test_url['menu'].format('all_menus')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(all_menus)
    for index, data in enumerate(content):
        for key, value in data.items():
            assert value == getattr(all_menus[index], key)


async def test_create_menu(
    client: AsyncClient, get_test_url: dict[str, str], test_db: AsyncSession
):
    data = create_menu_data()
    url = get_test_url['menu'].format('')
    response = await client.post(url=url, json=data.dict())
    assert response.status_code == 201
    content = response.json()
    assert content['title'] == data.title
    assert content['description'] == data.description
    assert 'id' in content
    assert 'submenus_count' in content
    assert 'dishes_count' in content


async def test_get_menu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu = await create_menu(db=test_db)
    url = get_test_url['menu'].format(menu.id)
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    for key, value in content.items():
        assert value == getattr(menu, key)


async def test_get_non_existent_menu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format(str(uuid.uuid4()))
    response = await client.get(url=url)
    assert response.status_code == 404


async def test_get_list_menus(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menus = await create_multi_menus(db=test_db)
    url = get_test_url['menu'].format('')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(menus)
    for index, data in enumerate(content):
        for key, value in data.items():
            assert value == getattr(menus[index], key)


async def test_update_menu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    update_data = create_menu_data()
    menu = await create_menu(db=test_db)
    url = get_test_url['menu'].format(menu.id)
    response = await client.patch(url=url, json=update_data.dict())
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == menu.id
    assert content['submenus_count'] == menu.submenus_count
    assert content['dishes_count'] == menu.dishes_count
    assert content['title'] == update_data.title
    assert content['description'] == update_data.description


async def test_update_non_existent_menu(
    client: AsyncClient, get_test_url: dict[str, str]
):
    update_data = create_menu_data().dict()
    url = get_test_url['menu'].format(str(uuid.uuid4()))
    response = await client.patch(url=url, json=update_data)
    assert response.status_code == 404


async def test_delete_menu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu = await create_menu(db=test_db)
    url = get_test_url['menu'].format(menu.id)
    response = await client.delete(url=url)
    assert response.status_code == 200
    response = await client.delete(url=url)
    assert response.status_code == 404


async def test_delete_non_existent_menu(
    client: AsyncClient, get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format(str(uuid.uuid4()))
    response = await client.delete(url=url)
    assert response.status_code == 404
