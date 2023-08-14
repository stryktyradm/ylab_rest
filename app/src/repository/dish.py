from src.models import Dish
from src.repository.base import BaseCRUDRepository
from src.schemas import DishCreate, DishRead, DishUpdate


class DishCRUDRepository(BaseCRUDRepository[Dish, DishCreate, DishRead, DishUpdate]):
    pass
