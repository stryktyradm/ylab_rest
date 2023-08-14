from pydantic import BaseModel
from src.schemas.dish import DishRead


class SubMenuBase(BaseModel):
    title: str | None
    description: str | None


class NestedSubMenu(SubMenuBase):
    id: str
    all_dishes: list[DishRead]


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuRead(SubMenuBase):
    id: str
    dishes_count: int


class SubMenuUpdate(SubMenuBase):
    pass
