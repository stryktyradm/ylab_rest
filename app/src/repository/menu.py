from src.models import Menu
from src.repository.base import BaseCRUDRepository
from src.schemas import MenuCreate, MenuUpdate


class MenuCRUDRepository(BaseCRUDRepository[Menu, MenuCreate, MenuUpdate]):
    pass
