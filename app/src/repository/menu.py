from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.models import Menu, SubMenu
from src.repository.base import BaseCRUDRepository
from src.schemas import (
    DishRead,
    MenuCreate,
    MenuRead,
    MenuUpdate,
    NestedMenu,
    NestedSubMenu,
)


class MenuCRUDRepository(BaseCRUDRepository[Menu, MenuCreate, MenuRead, MenuUpdate]):

    @staticmethod
    def process_nested_data(menu_items: Menu) -> NestedMenu:
        submenus = []
        for submenu in menu_items.submenus:
            dishes = [DishRead(**jsonable_encoder(dish)) for dish in submenu.dishes]
            submenu_nested = NestedSubMenu(**jsonable_encoder(submenu), all_dishes=dishes)
            submenus.append(submenu_nested)
        return NestedMenu(**jsonable_encoder(menu_items), all_submenus=submenus)

    def process_db_data(self, menu_obj: Menu) -> MenuRead:
        data = {
            **jsonable_encoder(menu_obj),
            'submenus_count': len(menu_obj.submenus),
            'dishes_count': sum(len(submenu.dishes) for submenu in menu_obj.submenus)
        }
        return self.schema.parse_obj(data)

    async def get_all_menus(self, as_dict: bool = False) -> list[NestedMenu] | dict[str, NestedMenu]:
        stmt = select(Menu).options(joinedload(Menu.submenus).joinedload(SubMenu.dishes))
        result = await self.db_session.execute(stmt)
        all_menus = result.unique().scalars().all()
        if as_dict:
            return {menu.id: self.process_nested_data(menu) for menu in all_menus}
        return [self.process_nested_data(menu) for menu in all_menus]
