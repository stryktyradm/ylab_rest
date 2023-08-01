from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.tests.utils import (
    create_menu,
    create_submenu,
    create_multi_submenus,
    random_lower_string
)


def test_create_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    menu = create_menu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, "")
    response = client.post(url=url, json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "dishes_count" in content


def tests_create_dish_in_non_existent_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    _, _ = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(999, "")
    response = client.post(url=url, json=data)
    assert response.status_code == 404


def test_get_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, submenu.id)
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    for key, value in content.items():
        assert value == getattr(submenu, key)


def test_get_non_existent_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, _ = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, 999)
    response = client.get(url=url)
    assert response.status_code == 404


def test_get_list_submenus(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenus = create_multi_submenus(db=get_db)
    url = get_test_url["submenu"].format(menu.id, "")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(submenus)
    for data in content:
        assert data in submenus


def test_get_list_submenus_in_non_existent_menu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    _, _ = create_multi_submenus(db=get_db)
    url = get_test_url["submenu"].format(999, "")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0


def test_update_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    update_data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    menu, submenu = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, submenu.id)
    response = client.patch(url=url, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == submenu.id
    assert content["dishes_count"] == submenu.dishes_count
    assert content["title"] == update_data["title"]
    assert content["description"] == update_data["description"]


def test_update_non_existent_submenu(
        client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    update_data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    menu, _ = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, 999)
    response = client.patch(url=url, json=update_data)
    assert response.status_code == 404


def test_delete_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, submenu = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, submenu.id)
    response = client.delete(url=url)
    assert response.status_code == 200


def test_delete_non_existent_submenu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu, _ = create_submenu(db=get_db)
    url = get_test_url["submenu"].format(menu.id, 999)
    response = client.get(url=url)
    assert response.status_code == 404
