from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.db.cache import get_cache_connection
from src.db.session import get_db
from src.repository.cache import BaseCacheRepository
from src.repository.dish import DishCRUDRepository
from src.repository.menu import MenuCRUDRepository
from src.repository.submenu import SubMenuCRUDRepository


async def get_menu_repository(db: AsyncSession = Depends(get_db)) -> MenuCRUDRepository:
    return MenuCRUDRepository(model=models.Menu, db_session=db)


async def get_submenu_repository(db: AsyncSession = Depends(get_db)) -> SubMenuCRUDRepository:
    return SubMenuCRUDRepository(model=models.SubMenu, db_session=db)


async def get_dish_repository(db: AsyncSession = Depends(get_db)) -> DishCRUDRepository:
    return DishCRUDRepository(model=models.Dish, db_session=db)


async def get_cache_repository(cache_conn: Redis = Depends(get_cache_connection)) -> BaseCacheRepository:
    return BaseCacheRepository(cache=cache_conn)
