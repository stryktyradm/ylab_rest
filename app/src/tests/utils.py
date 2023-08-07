import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from src import models, schemas
from src.repository import (
    get_dish_repository,
    get_menu_repository,
    get_submenu_repository,
)


def random_lower_string() -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=32))


def random_float_number() -> float:
    return round(random.uniform(1, 100), 2)


def create_title_and_description() -> tuple[str, str]:
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


async def create_menu(db: AsyncSession) -> models.Menu:
    menu_in = create_menu_data()
    repo = await get_menu_repository(db=db)
    menu = await repo.create(obj_in=menu_in)
    return menu


async def create_multi_menus(db: AsyncSession, count: int = 3) -> list[models.Menu]:
    menus = list()
    for _ in range(count):
        menu = await create_menu(db)
        menus.append(menu)
    return menus


async def create_submenu(db: AsyncSession) -> tuple[models.Menu, models.SubMenu]:
    menu = await create_menu(db=db)
    submenu_in = create_submenu_data()
    repo = await get_submenu_repository(db=db)
    submenu = await repo.create(obj_in=submenu_in, menu_id=menu.id)
    return menu, submenu


async def create_multi_submenus(
    db: AsyncSession, count: int = 3
) -> tuple[models.Menu, list[models.SubMenu]]:
    menu = await create_menu(db=db)
    submenus = list()
    for _ in range(count):
        submenu_in = create_submenu_data()
        repo = await get_submenu_repository(db=db)
        submenu = await repo.create(obj_in=submenu_in, menu_id=menu.id)
        submenus.append(submenu)
    return menu, submenus


async def create_dish(db: AsyncSession) -> tuple[models.Menu, models.SubMenu, models.Dish]:
    menu, submenu = await create_submenu(db=db)
    dish_in = create_dish_data()
    repo = await get_dish_repository(db=db)
    dish = await repo.create(obj_in=dish_in, submenu_id=submenu.id)
    return menu, submenu, dish


async def create_multi_dishes(
    db: AsyncSession, count: int = 3
) -> tuple[models.Menu, models.SubMenu, list[models.Dish]]:
    menu, submenu = await create_submenu(db=db)
    dishes = list()
    for _ in range(count):
        dish_in = create_dish_data()
        repo = await get_dish_repository(db=db)
        dish = await repo.create(obj_in=dish_in, submenu_id=submenu.id)
        dishes.append(dish)
    return menu, submenu, dishes
