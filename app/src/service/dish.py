from src.schemas.dish import DishCreate, DishRead, DishUpdate
from src.service.base import BaseService


class DishService(BaseService[DishCreate, DishRead, DishUpdate]):
    pass
