from src.crud.base import CRUDBase
from src.models import Dish
from src.schemas import DishCreate, DishRead, DishUpdate


class CRUDDish(CRUDBase[Dish, DishCreate, DishUpdate]):
    pass


dish = CRUDDish(Dish, DishRead)
