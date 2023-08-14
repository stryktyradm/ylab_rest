from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas
from src.db.cache import get_cache_connection
from src.db.session import get_db
from src.repository.cache import BaseCacheRepository
from src.repository.dish import DishCRUDRepository
from src.repository.menu import MenuCRUDRepository
from src.repository.submenu import SubMenuCRUDRepository


async def get_menu_repository(db: AsyncSession = Depends(get_db)) -> MenuCRUDRepository:
    return MenuCRUDRepository(
        model=models.Menu, schema=schemas.MenuRead, db_session=db
    )


async def get_submenu_repository(db: AsyncSession = Depends(get_db)) -> SubMenuCRUDRepository:
    return SubMenuCRUDRepository(
        model=models.SubMenu, schema=schemas.SubMenuRead, db_session=db
    )


async def get_dish_repository(db: AsyncSession = Depends(get_db)) -> DishCRUDRepository:
    return DishCRUDRepository(
        model=models.Dish, schema=schemas.DishRead, db_session=db
    )


async def get_cache_repository(
        cache_conn: Redis = Depends(get_cache_connection)
) -> BaseCacheRepository:
    return BaseCacheRepository(cache=cache_conn)
