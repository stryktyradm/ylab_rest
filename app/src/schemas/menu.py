from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str | None
    description: str | None


class MenuCreate(MenuBase):
    pass


class MenuRead(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int


class MenuUpdate(MenuBase):
    pass
