from fastapi.encoders import jsonable_encoder
from src.models import SubMenu
from src.schemas.submenu import SubMenuCreate, SubMenuRead, SubMenuUpdate
from src.service.base import BaseService


class SubMenuService(BaseService[SubMenuCreate, SubMenuRead, SubMenuUpdate]):
    def process_db_data(self, submenu_obj: SubMenu) -> SubMenuRead:
        data = {
            **jsonable_encoder(submenu_obj),
            'dishes_count': len(submenu_obj.dishes)
        }
        return self.schema.parse_obj(data)
