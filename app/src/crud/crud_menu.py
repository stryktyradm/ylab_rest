from fastapi.encoders import jsonable_encoder

from src.crud.base import CRUDBase
from src.models import Menu
from src.schemas import MenuCreate, MenuRead, MenuUpdate


class CRUDMenu(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    def process_data_from_db(self, menu_obj: Menu):
        data = {
            **jsonable_encoder(menu_obj),
            "submenus_count": len(menu_obj.submenus),
            "dishes_count": sum([len(submenu.dishes) for submenu in menu_obj.submenus])
        }
        return self.schema.parse_obj(data)


menu = CRUDMenu(Menu, MenuRead)
