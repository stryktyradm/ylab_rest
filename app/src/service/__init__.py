from fastapi import Depends

from src import schemas
from src.repository import (
    get_menu_repository,
    get_submenu_repository,
    get_dish_repository,
    get_cache_repository,
    BaseCacheRepository
)
from src.service.dish import DishService, DishRepository
from src.service.menu import MenuService, MenuRepository
from src.service.submenu import SubMenuService, SubMenuRepository


async def get_menu_service(
    repo: type[MenuRepository] = Depends(get_menu_repository),
    cache: BaseCacheRepository = Depends(get_cache_repository)
) -> MenuService:
    return MenuService(
        repo=repo,
        schema=schemas.MenuRead,
        cache=cache,
        cache_mask='{id_}',
        cache_root='menus',
        cache_namespace='menus',
    )


async def get_submenu_service(
    repo: type[SubMenuRepository] = Depends(get_submenu_repository),
    cache: BaseCacheRepository = Depends(get_cache_repository)
) -> SubMenuService:
    return SubMenuService(
        repo=repo,
        schema=schemas.SubMenuRead,
        cache=cache,
        cache_mask='{menu_id}:{id_}',
        cache_root='menus',
        cache_namespace='{menu_id}:submenus',
    )


async def get_dish_service(
    repo: type[DishRepository] = Depends(get_dish_repository),
    cache: BaseCacheRepository = Depends(get_cache_repository)
) -> DishService:
    return DishService(
        repo=repo,
        schema=schemas.DishRead,
        cache=cache,
        cache_mask='{menu_id}:{submenu_id}:{id_}',
        cache_root='menus',
        cache_namespace='{menu_id}:{submenu_id}:dishes'
    )
