from fastapi.encoders import jsonable_encoder
from src.models import Menu
from src.schemas.menu import MenuCreate, MenuRead, MenuUpdate
from src.service.base import BaseService


class MenuService(BaseService[MenuCreate, MenuRead, MenuUpdate]):
    def process_db_data(self, menu_obj: Menu) -> MenuRead:
        data = {
            **jsonable_encoder(menu_obj),
            'submenus_count': len(menu_obj.submenus),
            'dishes_count': sum(len(submenu.dishes) for submenu in menu_obj.submenus)
        }
        return self.schema.parse_obj(data)
