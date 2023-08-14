import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.tests.utils import create_dish, create_multi_dishes

# async def test_create_dish(
#     client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
# ):
#     data = create_dish_data()
#     menu, submenu = await create_submenu(db=test_db)
#     url = get_test_url['dish'].format(menu.id, submenu.id, '')
#     response = await client.post(url=url, json=data.dict())
#     assert response.status_code == 201
#     content = response.json()
#     assert content['title'] == data.title
#     assert content['description'] == data.description
#     assert content['price'] == str(data.price)
#     assert 'id' in content
#
#
# async def tests_create_dish_in_non_existent_submenu(
#     client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
# ):
#     data = create_dish_data()
#     menu, _ = await create_submenu(db=test_db)
#     url = get_test_url['dish'].format(menu.id, str(uuid.uuid4()), '')
#     response = await client.post(url=url, json=data.dict())
#     assert response.status_code == 404


async def test_get_dish(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu, dish = await create_dish(db=test_db)
    url = get_test_url['dish'].format(menu.id, submenu.id, dish.id)
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    for key, value in content.items():
        assert value == getattr(dish, key)


async def test_get_non_existent_dish(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu, _ = await create_dish(db=test_db)
    url = get_test_url['dish'].format(menu.id, submenu.id, str(uuid.uuid4()))
    response = await client.get(url=url)
    assert response.status_code == 404


async def test_get_list_dishes(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu, dishes = await create_multi_dishes(db=test_db)
    url = get_test_url['dish'].format(menu.id, submenu.id, '')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(dishes)
    for index, data in enumerate(content):
        for key, value in data.items():
            assert value == getattr(dishes[index], key)


async def test_get_list_dishes_in_non_existent_submenu(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, _, _ = await create_multi_dishes(db=test_db)
    url = get_test_url['dish'].format(menu.id, str(uuid.uuid4()), '')
    response = await client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0


# async def test_update_dish(
#     client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
# ):
#     update_data = create_dish_data()
#     menu, submenu, dish = await create_dish(db=test_db)
#     url = get_test_url['dish'].format(menu.id, submenu.id, dish.id)
#     response = await client.patch(url=url, json=update_data.dict())
#     assert response.status_code == 200
#     content = response.json()
#     assert content['id'] == dish.id
#     assert content['title'] == update_data.title
#     assert content['description'] == update_data.description
#     assert content['price'] == str(update_data.price)
#
#
# async def test_update_non_existent_dish(
#     client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
# ):
#     update_data = create_dish_data()
#     menu, submenu, _ = await create_dish(db=test_db)
#     url = get_test_url['dish'].format(menu.id, submenu.id, str(uuid.uuid4()))
#     response = await client.patch(url=url, json=update_data.dict())
#     assert response.status_code == 404


async def test_delete_dish(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu, dish = await create_dish(db=test_db)
    url = get_test_url['dish'].format(menu.id, submenu.id, dish.id)
    response = await client.delete(url=url)
    assert response.status_code == 200


async def test_delete_non_existent_dish(
    client: AsyncClient, test_db: AsyncSession, get_test_url: dict[str, str]
):
    menu, submenu, _ = await create_dish(db=test_db)
    url = get_test_url['dish'].format(menu.id, submenu.id, str(uuid.uuid4()))
    response = await client.delete(url=url)
    assert response.status_code == 404
