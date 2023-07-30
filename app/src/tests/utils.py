import random
import string
from typing import Tuple

from sqlalchemy.orm import Session

from src import crud
from src import schemas


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_float_number() -> float:
    return round(random.uniform(1, 100), 2)


def create_title_and_description() -> Tuple[str, str]:
    return random_lower_string(), random_lower_string()


def create_menu_data() -> schemas.MenuCreate:
    title, description = create_title_and_description()
    menu_in = schemas.MenuCreate(
        title=title,
        description=description
    )
    return menu_in


def create_submenu_data() -> schemas.SubMenuCreate:
    title, description = create_title_and_description()
    submenu_in = schemas.SubMenuCreate(
        title=title,
        description=description
    )
    return submenu_in


def create_dish_data() -> schemas.DishCreate:
    title, description = create_title_and_description()
    price = random_float_number()
    dish_in = schemas.DishCreate(
        title=title,
        description=description,
        price=price
    )
    return dish_in


def create_menu(db: Session) -> schemas.MenuRead:
    menu_in = create_menu_data()
    menu = crud.menu.create(db=db, obj_in=menu_in)
    return menu


def create_multi_menus(db: Session, count: int = 3) -> list[schemas.MenuRead]:
    menus = list()
    for _ in range(count):
        menus.append(create_menu(db))
    return menus


def create_submenu(db: Session) -> Tuple[schemas.MenuRead, schemas.SubMenuRead]:
    menu = create_menu(db=db)
    submenu_in = create_submenu_data()
    submenu = crud.submenu.create(db=db, obj_in=submenu_in, menu_id=menu.id)
    return menu, submenu


def create_multi_submenus(
        db: Session, count: int = 3
) -> Tuple[schemas.MenuRead, list[schemas.SubMenuRead]]:
    menu = create_menu(db=db)
    submenus = list()
    for _ in range(count):
        submenu_in = create_submenu_data()
        submenu = crud.submenu.create(db=db, obj_in=submenu_in, menu_id=menu.id)
        submenus.append(submenu)
    return menu, submenus


def create_dish(db: Session) -> Tuple[schemas.MenuRead, schemas.SubMenuRead, schemas.DishRead]:
    menu, submenu = create_submenu(db=db)
    dish_in = create_dish_data()
    dish = crud.dish.create(db=db, obj_in=dish_in, submenu_id=submenu.id)
    return menu, submenu, dish


def create_multi_dishes(
        db: Session, count: int = 3
) -> Tuple[schemas.MenuRead, schemas.SubMenuRead, list[schemas.DishRead]]:
    menu, submenu = create_submenu(db=db)
    dishes = list()
    for _ in range(count):
        dish_in = create_dish_data()
        dish = crud.dish.create(db=db, obj_in=dish_in, submenu_id=submenu.id)
        dishes.append(dish)
    return menu, submenu, dishes
