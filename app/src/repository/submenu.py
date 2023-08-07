from src.models import SubMenu
from src.repository.base import BaseCRUDRepository
from src.schemas import SubMenuCreate, SubMenuUpdate


class SubMenuCRUDRepository(BaseCRUDRepository[SubMenu, SubMenuCreate, SubMenuUpdate]):
    pass
