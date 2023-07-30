from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.tests.utils import random_lower_string, random_float_number


def test_create_menu(
    client: TestClient, get_db: Session,
    ids: dict[str, id], get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    url = get_test_url["menu"].format("")
    response = client.post(url=url, json=data)
    ids["menu"] += 1
    assert response.status_code == 201
    content = response.json()
    assert content["id"] == str(ids["menu"])


def test_create_submenu(
    client: TestClient, get_db: Session,
    ids: dict, get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string()
    }
    url = get_test_url["submenu"].format(ids["menu"], "")
    response = client.post(url=url, json=data)
    ids["submenu"] += 1
    assert response.status_code == 201
    content = response.json()
    assert content["id"] == str(ids["submenu"])


def test_create_dish_1(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "price": random_float_number()
    }
    url = get_test_url["dish"].format(ids["menu"], ids["submenu"], "")
    response = client.post(url=url, json=data)
    ids["dish"] += 1
    assert response.status_code == 201
    content = response.json()
    assert content["id"] == str(ids["dish"])


def test_create_dish_2(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "price": random_float_number()
    }
    url = get_test_url["dish"].format(ids["menu"], ids["submenu"], "")
    response = client.post(url=url, json=data)
    ids["dish"] += 1
    assert response.status_code == 201
    content = response.json()
    assert content["id"] == str(ids["dish"])


def test_get_menu(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["menu"].format(ids["menu"])
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(ids["menu"])
    assert content["submenus_count"] == 1
    assert content["dishes_count"] == 2


def test_get_submenu(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["submenu"].format(ids["menu"], ids["submenu"])
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(ids["submenu"])
    assert content["dishes_count"] == 2


def test_delete_submenu(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["submenu"].format(ids["menu"], ids["submenu"])
    response = client.delete(url=url)
    assert response.status_code == 200


def test_get_submenus(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["submenu"].format(ids["menu"], "")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0


def test_get_dishes(
        client: TestClient, get_db: Session,
        ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["dish"].format(ids["menu"], ids["submenu"], "")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0


def test_get_menu_after_delete(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["menu"].format(ids["menu"])
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(ids['menu'])
    assert content["submenus_count"] == 0
    assert content["dishes_count"] == 0


def test_delete_menu(
    client: TestClient, get_db: Session,
    ids: dict[str, int], get_test_url: dict[str, str]
):
    url = get_test_url["menu"].format(ids["menu"])
    response = client.delete(url=url)
    assert response.status_code == 200


def test_get_menus(
    client: TestClient, get_db: Session, get_test_url: dict[str, str]
):
    url = get_test_url["menu"].format("")
    response = client.get(url=url)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0
