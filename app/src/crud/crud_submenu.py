from fastapi.encoders import jsonable_encoder

from src.crud.base import CRUDBase
from src.models import SubMenu
from src.schemas import SubMenuCreate, SubMenuRead, SubMenuUpdate


class CRUDSubMenu(CRUDBase[SubMenu, SubMenuCreate, SubMenuUpdate]):
    def process_data_from_db(self, submenu_obj: SubMenu):
        data = {
            **jsonable_encoder(submenu_obj),
            "dishes_count": len(submenu_obj.dishes)
        }
        return self.schema.parse_obj(data)


submenu = CRUDSubMenu(SubMenu, SubMenuRead)
