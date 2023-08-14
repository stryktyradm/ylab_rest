import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
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


async def create_menu(db: AsyncSession) -> schemas.MenuRead:
    menu_in = create_menu_data()
    repo = await get_menu_repository(db=db)
    menu = await repo.create(obj_in=menu_in)
    return menu


async def create_multi_menus(db: AsyncSession, count: int = 3) -> list[schemas.MenuRead]:
    menus = list()
    for _ in range(count):
        menu = await create_menu(db)
        menus.append(menu)
    return menus


async def create_submenu(db: AsyncSession) -> tuple[schemas.MenuRead, schemas.SubMenuRead]:
    menu = await create_menu(db=db)
    submenu_in = create_submenu_data()
    repo = await get_submenu_repository(db=db)
    submenu = await repo.create(obj_in=submenu_in, menu_id=menu.id)
    return menu, submenu


async def create_multi_submenus(
    db: AsyncSession, count: int = 3
) -> tuple[schemas.MenuRead, list[schemas.SubMenuRead]]:
    menu = await create_menu(db=db)
    submenus = list()
    for _ in range(count):
        submenu_in = create_submenu_data()
        repo = await get_submenu_repository(db=db)
        submenu = await repo.create(obj_in=submenu_in, menu_id=menu.id)
        submenus.append(submenu)
    return menu, submenus


async def create_dish(
    db: AsyncSession
) -> tuple[schemas.MenuRead, schemas.SubMenuRead, schemas.DishRead]:
    menu, submenu = await create_submenu(db=db)
    dish_in = create_dish_data()
    repo = await get_dish_repository(db=db)
    dish = await repo.create(obj_in=dish_in, submenu_id=submenu.id)
    return menu, submenu, dish


async def create_multi_dishes(
    db: AsyncSession, count: int = 3
) -> tuple[schemas.MenuRead, schemas.SubMenuRead, list[schemas.DishRead]]:
    menu, submenu = await create_submenu(db=db)
    dishes = list()
    for _ in range(count):
        dish_in = create_dish_data()
        repo = await get_dish_repository(db=db)
        dish = await repo.create(obj_in=dish_in, submenu_id=submenu.id)
        dishes.append(dish)
    return menu, submenu, dishes


async def create_menu_with_nested_data(db: AsyncSession) -> list[schemas.NestedMenu]:
    menus = []
    menu_repo = await get_menu_repository(db=db)
    submenu_repo = await get_submenu_repository(db=db)
    dish_repo = await get_dish_repository(db=db)
    for i in range(2):
        menu_data = create_menu_data()
        menu = await menu_repo.create(obj_in=menu_data)
        submenus = []
        for j in range(2):
            submenu_data = create_submenu_data()
            submenu = await submenu_repo.create(obj_in=submenu_data, menu_id=menu.id)
            dishes = []
            for k in range(3):
                dish_data = create_dish_data()
                dish = await dish_repo.create(obj_in=dish_data, submenu_id=submenu.id)
                dishes.append(dish)
            submenu_with_dishes = schemas.NestedSubMenu(
                id=submenu.id, title=submenu.title, description=submenu.description, all_dishes=dishes
            )
            submenus.append(submenu_with_dishes)
        menu_with_submenus_and_dishes = schemas.NestedMenu(
            id=menu.id, title=menu.title, description=menu.description, all_submenus=submenus
        )
        menus.append(menu_with_submenus_and_dishes)
    return menus
