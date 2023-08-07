import pytest
from httpx import AsyncClient
from src.tests.utils import random_float_number, random_lower_string


@pytest.mark.order(1)
async def test_create_menu(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    data = {
        'title': random_lower_string(),
        'description': random_lower_string()
    }
    url = get_test_url['menu'].format('')
    response = await client.post(url=url, json=data)
    ids['menu'] = response.json()['id']
    assert response.status_code == 201
    content = response.json()
    assert content['id'] == str(ids['menu'])


@pytest.mark.order(2)
async def test_create_submenu(
    client: AsyncClient, ids: dict, get_test_url: dict[str, str]
):
    data = {
        'title': random_lower_string(),
        'description': random_lower_string()
    }
    url = get_test_url['submenu'].format(ids['menu'], '')
    response = await client.post(url=url, json=data)
    ids['submenu'] = response.json()['id']
    assert response.status_code == 201
    content = response.json()
    assert content['id'] == str(ids['submenu'])


@pytest.mark.order(3)
async def test_create_dish_1(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    data = {
        'title': random_lower_string(),
        'description': random_lower_string(),
        'price': random_float_number()
    }
    url = get_test_url['dish'].format(ids['menu'], ids['submenu'], '')
    response = await client.post(url=url, json=data)
    ids['dish_1'] = response.json()['id']
    assert response.status_code == 201
    content = response.json()
    assert content['id'] == str(ids['dish_1'])


@pytest.mark.order(4)
async def test_create_dish_2(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    data = {
        'title': random_lower_string(),
        'description': random_lower_string(),
        'price': random_float_number()
    }
    url = get_test_url['dish'].format(ids['menu'], ids['submenu'], '')
    response = await client.post(url=url, json=data)
    ids['dish_2'] = response.json()['id']
    assert response.status_code == 201
    content = response.json()
    assert content['id'] == str(ids['dish_2'])


@pytest.mark.order(5)
async def test_get_menu(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format(ids['menu'])
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == str(ids['menu'])
    assert content['submenus_count'] == 1
    assert content['dishes_count'] == 2


@pytest.mark.order(6)
async def test_get_submenu(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['submenu'].format(ids['menu'], ids['submenu'])
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == str(ids['submenu'])
    assert content['dishes_count'] == 2


@pytest.mark.order(7)
async def test_delete_submenu(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['submenu'].format(ids['menu'], ids['submenu'])
    response = await client.delete(url=url)
    assert response.status_code == 200


@pytest.mark.order(8)
async def test_get_submenus(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['submenu'].format(ids['menu'], '')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0


@pytest.mark.order(9)
async def test_get_dishes(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['dish'].format(ids['menu'], ids['submenu'], '')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0


@pytest.mark.order(10)
async def test_get_menu_after_delete(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format(ids['menu'])
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert content['id'] == str(ids['menu'])
    assert content['submenus_count'] == 0
    assert content['dishes_count'] == 0


@pytest.mark.order(11)
async def test_delete_menu(
    client: AsyncClient, ids: dict[str, str], get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format(ids['menu'])
    response = await client.delete(url=url)
    assert response.status_code == 200


@pytest.mark.order(12)
async def test_get_menus(
    client: AsyncClient, get_test_url: dict[str, str]
):
    url = get_test_url['menu'].format('')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0
