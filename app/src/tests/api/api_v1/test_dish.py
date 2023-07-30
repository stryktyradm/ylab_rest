from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.tests.utils import (
    create_submenu,
    create_dish,
    create_multi_dishes,
    random_lower_string,
    random_float_number
)


def test_create_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "price": random_float_number()
    }
    menu, submenu = create_submenu(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, "")
    response = client.post(url=url, json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["price"] == str(data["price"])
    assert "id" in content


def tests_create_dish_in_non_existent_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "price": random_float_number()
    }
    menu, _ = create_submenu(db=get_db)
    url = get_test_url["dish"].format(menu.id, 999, "")
    response = client.post(url=url, json=data)
    assert response.status_code == 404


def test_get_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu, dish = create_dish(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, dish.id)
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    for key, value in content.items():
        assert value == getattr(dish, key)


def test_get_non_existent_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu, _ = create_dish(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, 999)
    response = client.get(url=url)
    assert response.status_code == 404


def test_get_list_dishes(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu, dishes = create_multi_dishes(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, "")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(dishes)
    for index, data in enumerate(content):
        for key, value in data.items():
            assert value == getattr(dishes[index], key)


def test_get_list_dishes_in_non_existent_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, _, _ = create_multi_dishes(db=get_db)
    url = get_test_url["dish"].format(menu.id, 999, "")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0


def test_update_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    update_data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "price": random_float_number()
    }
    menu, submenu, dish = create_dish(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, dish.id)
    response = client.patch(url=url, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == dish.id
    assert content["title"] == update_data["title"]
    assert content["description"] == update_data["description"]
    assert content["price"] == str(update_data["price"])


def test_update_non_existent_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    update_data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "price": random_float_number()
    }
    menu, submenu, _ = create_dish(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, 999)
    response = client.patch(url=url, json=update_data)
    assert response.status_code == 404


def test_delete_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu, dish = create_dish(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, dish.id)
    response = client.delete(url=url)
    assert response.status_code == 200


def test_delete_non_existent_dish(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu, _ = create_dish(db=get_db)
    url = get_test_url["dish"].format(menu.id, submenu.id, 999)
    response = client.delete(url=url)
    assert response.status_code == 404
