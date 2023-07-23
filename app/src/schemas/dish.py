from pydantic import BaseModel
from pydantic.types import condecimal


class DishBase(BaseModel):
    title: str | None
    description: str | None
    price: condecimal(decimal_places=2)


class DishCreate(DishBase):
    pass


class DishRead(DishBase):
    id: str
    price: str


class DishUpdate(DishBase):
    pass
