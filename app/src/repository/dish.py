from src.models import Dish
from src.repository.base import BaseCRUDRepository
from src.schemas import DishCreate, DishUpdate


class DishCRUDRepository(BaseCRUDRepository[Dish, DishCreate, DishUpdate]):
    pass
