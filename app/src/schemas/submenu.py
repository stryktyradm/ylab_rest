from pydantic import BaseModel


class SubMenuBase(BaseModel):
    title: str | None
    description: str | None


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuRead(SubMenuBase):
    id: str
    dishes_count: int


class SubMenuUpdate(SubMenuBase):
    pass
