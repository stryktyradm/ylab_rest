from typing import TypeVar

from src.repository.menu import MenuCRUDRepository
from src.schemas.menu import MenuCreate, MenuRead, MenuUpdate, NestedMenu
from src.service.base import BaseService

MenuRepository = TypeVar('MenuRepository', bound=MenuCRUDRepository)


class MenuService(BaseService[MenuRepository, MenuCreate, MenuRead, MenuUpdate]):
    async def get_all_items(self) -> list[NestedMenu] | dict[str, NestedMenu]:
        items = await self.repo.get_all_menus()  # type: ignore
        return items
