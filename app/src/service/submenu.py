from typing import TypeVar

from src.repository.submenu import SubMenuCRUDRepository
from src.schemas.submenu import SubMenuCreate, SubMenuRead, SubMenuUpdate
from src.service.base import BaseService

SubMenuRepository = TypeVar('SubMenuRepository', bound=SubMenuCRUDRepository)


class SubMenuService(BaseService[SubMenuRepository, SubMenuCreate, SubMenuRead, SubMenuUpdate]):
    pass
