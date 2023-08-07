import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.tests.utils import create_menu, create_multi_menus, random_lower_string


async def test_create_menu(
    client: AsyncClient, get_test_url: dict[str, str], test_db: AsyncSession
):
    data = {
        'title': random_lower_string(),
        'description': random_lower_string()
    }
    url = get_test_url['menu'].format('')
    response = await client.post(url=url, json=data)
    assert response.status_code == 201
    content = response.json()
    assert content['title'] == data['title']
    assert content['description'] == data['description']
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
    assert menu.id == content['id']


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


async def test_update_menu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    update_data = {
        'title': random_lower_string(),
        'description': random_lower_string()
    }
    menu = await create_menu(db=test_db)
    url = get_test_url['menu'].format(menu.id)
    response = await client.patch(url=url, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == menu.id
    assert content['submenus_count'] == len(menu.submenus)
    assert content['dishes_count'] == sum(len(submenu.dishes) for submenu in menu.submenus)
    assert content['title'] == update_data['title']
    assert content['description'] == update_data['description']


async def test_update_non_existent_menu(
    client: AsyncClient, get_test_url: dict[str, str]
):
    update_data = {
        'title': random_lower_string(),
        'description': random_lower_string()
    }
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


async def test_delete_non_existent_menu(
    client: AsyncClient, get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format(str(uuid.uuid4()))
    response = await client.delete(url=url)
    assert response.status_code == 404
