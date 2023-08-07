from fastapi import Depends

from src import schemas

from src.repository import (
    get_menu_repository, MenuCRUDRepository,
    get_submenu_repository, SubMenuCRUDRepository,
    get_dish_repository, DishCRUDRepository,
    get_cache_repository, BaseCacheRepository
)

from src.service.dish import DishService
from src.service.menu import MenuService
from src.service.submenu import SubMenuService


async def get_menu_service(
    repo: MenuCRUDRepository = Depends(get_menu_repository),
    cache: BaseCacheRepository = Depends(get_cache_repository)
) -> MenuService:
    return MenuService(
        repo=repo,
        schema=schemas.MenuRead,
        cache=cache,
        cache_namespace='menu',
        linked_cache_namespace=['submenu', 'dish']
    )


async def get_submenu_service(
    repo: SubMenuCRUDRepository = Depends(get_submenu_repository),
    cache: BaseCacheRepository = Depends(get_cache_repository)
) -> SubMenuService:
    return SubMenuService(
        repo=repo,
        schema=schemas.SubMenuRead,
        cache=cache,
        cache_namespace='submenu',
        linked_cache_namespace=['menu', 'dish']
    )


async def get_dish_service(
    repo: DishCRUDRepository = Depends(get_dish_repository),
    cache: BaseCacheRepository = Depends(get_cache_repository)
) -> DishService:
    return DishService(
        repo=repo,
        schema=schemas.DishRead,
        cache=cache,
        cache_namespace='dish',
        linked_cache_namespace=['menu', 'submenu']
    )
