from pydantic import BaseModel
from src.schemas.submenu import NestedSubMenu


class MenuBase(BaseModel):
    title: str | None
    description: str | None


class NestedMenu(MenuBase):
    id: str
    all_submenus: list[NestedSubMenu]


class MenuCreate(MenuBase):
    pass


class MenuRead(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int


class MenuUpdate(MenuBase):
    pass
