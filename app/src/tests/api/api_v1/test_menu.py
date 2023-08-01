from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.tests.utils import random_lower_string, create_menu, create_multi_menus


def test_create_menu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    url = get_test_url["menu"].format("")
    response = client.post(url=url, json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "submenus_count" in content
    assert "dishes_count" in content


def test_get_menu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu = create_menu(db=get_db)
    url = get_test_url["menu"].format(menu.id)
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    for key, value in content.items():
        assert value == getattr(menu, key)


def test_get_non_existent_menu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    url = get_test_url["menu"].format(999)
    response = client.get(url=url)
    assert response.status_code == 404


def test_get_list_menus(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menus = create_multi_menus(db=get_db)
    url = get_test_url["menu"].format("")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(menus)
    for data in content:
        assert data in menus


def test_update_menu(
        client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    update_data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    menu = create_menu(db=get_db)
    url = get_test_url["menu"].format(menu.id)
    response = client.patch(url=url, json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == menu.id
    assert content["submenus_count"] == menu.submenus_count
    assert content["dishes_count"] == menu.dishes_count
    assert content["title"] == update_data["title"]
    assert content["description"] == update_data["description"]


def test_update_non_existent_menu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    update_data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    url = get_test_url["menu"].format(999)
    response = client.patch(url=url, json=update_data)
    assert response.status_code == 404


def test_delete_menu(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    menu = create_menu(db=get_db)
    url = get_test_url["menu"].format(menu.id)
    response = client.delete(url=url)
    assert response.status_code == 200


def test_delete_non_existent_menu(
        client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    url = get_test_url["menu"].format(999)
    response = client.delete(url=url)
    assert response.status_code == 404
